package main

import (
	"context"
	"errors"
	"flag"
	"fmt"
	"net/http"
	"os"
	"os/signal"

	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"

	agentlog "trpc.group/trpc-go/trpc-agent-go/log"
	"trpc.group/trpc-go/trpc-agent-go/runner"
	"trpc.group/trpc-go/trpc-agent-go/server/agui"

	"trpcagentdemo/acp"
)

func main() {
	if err := run(); err != nil {
		fmt.Fprintln(os.Stderr, "error:", err)
		os.Exit(1)
	}
}

func run() error {
	mode := flag.String("mode", "both", "which protocols to serve: both | agui | acp")
	kind := flag.String("agent", "echo", "agent implementation: echo | llm")
	modelName := flag.String("model", "deepseek-v4-flash", "model name when -agent llm")
	stream := flag.Bool("stream", true, "stream model output when -agent llm")
	address := flag.String("address", "127.0.0.1:8080", "AG-UI listen address")
	path := flag.String("path", "/agui", "AG-UI HTTP path")
	flag.Parse()

	// ACP owns stdout. Framework logs default to stdout, so move them first.
	useStderrLogger()

	ag, err := newAgent(*kind, *modelName, *stream)
	if err != nil {
		return err
	}
	agentRunner := runner.NewRunner(ag.Info().Name, ag)
	defer agentRunner.Close()

	serveAGUI := *mode == "both" || *mode == "agui"
	serveACP := *mode == "both" || *mode == "acp"
	if !serveAGUI && !serveACP {
		return fmt.Errorf("unknown mode %q", *mode)
	}

	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt)
	defer stop()

	errCh := make(chan error, 1)
	if serveAGUI {
		server, err := agui.New(agentRunner, agui.WithPath(*path))
		if err != nil {
			return err
		}
		httpServer := &http.Server{Addr: *address, Handler: server.Handler()}
		go func() {
			<-ctx.Done()
			_ = httpServer.Close()
		}()
		go func() {
			fmt.Fprintf(os.Stderr, "AG-UI: %s on http://%s%s\n", ag.Info().Name, *address, server.Path())
			err := httpServer.ListenAndServe()
			if err != nil && !errors.Is(err, http.ErrServerClosed) {
				errCh <- err
			}
		}()
	}

	if serveACP {
		server, err := newACPServer(agentRunner)
		if err != nil {
			return err
		}
		fmt.Fprintf(os.Stderr, "ACP: %s on stdio\n", ag.Info().Name)
		if err := server.Serve(ctx, os.Stdin, os.Stdout); err != nil && !errors.Is(err, context.Canceled) {
			return err
		}
		return nil
	}

	select {
	case <-ctx.Done():
		return nil
	case err := <-errCh:
		return err
	}
}

func newACPServer(agentRunner runner.Runner) (*acp.Server, error) {
	return acp.New(
		agentRunner,
		acp.WithUserID("acp"),
		acp.WithImplementation("trpc-agent-go-dual", "0.1.0"),
	)
}

func useStderrLogger() {
	logger := zap.New(
		zapcore.NewCore(
			zapcore.NewConsoleEncoder(zap.NewDevelopmentEncoderConfig()),
			zapcore.AddSync(os.Stderr),
			zapcore.InfoLevel,
		),
		zap.AddCallerSkip(1),
	).Sugar()
	agentlog.Default = logger
	agentlog.ContextDefault = logger
}
