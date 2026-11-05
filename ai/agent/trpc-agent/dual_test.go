package main

import (
	"bufio"
	"context"
	"encoding/json"
	"errors"
	"io"
	"net"
	"net/http"
	"net/http/httptest"
	"strings"
	"sync"
	"testing"
	"time"

	acpsdk "github.com/coder/acp-go-sdk"

	"trpc.group/trpc-go/trpc-agent-go/runner"
	"trpc.group/trpc-go/trpc-agent-go/server/agui"

	"trpcagentdemo/acp"
)

func TestEchoAgentSpeaksACPAndAGUI(t *testing.T) {
	ag, err := newAgent("echo", "", false)
	if err != nil {
		t.Fatal(err)
	}
	agentRunner := runner.NewRunner(ag.Info().Name, ag)
	defer agentRunner.Close()

	t.Run("agui", func(t *testing.T) {
		server, err := agui.New(agentRunner, agui.WithPath("/agui"))
		if err != nil {
			t.Fatal(err)
		}
		httpServer := httptest.NewServer(server.Handler())
		defer httpServer.Close()

		body := `{"threadId":"thread-1","runId":"run-1","messages":[{"role":"user","content":"ping"}]}`
		req, err := http.NewRequest(http.MethodPost, httpServer.URL+server.Path(), strings.NewReader(body))
		if err != nil {
			t.Fatal(err)
		}
		req.Header.Set("Content-Type", "application/json")
		req.Header.Set("Accept", "text/event-stream")
		resp, err := httpServer.Client().Do(req)
		if err != nil {
			t.Fatal(err)
		}
		defer resp.Body.Close()
		if resp.StatusCode != http.StatusOK {
			payload, _ := io.ReadAll(resp.Body)
			t.Fatalf("status %s: %s", resp.Status, payload)
		}

		events, text := readAGUI(t, resp.Body)
		if !contains(events, "RUN_STARTED") || !contains(events, "RUN_FINISHED") {
			t.Fatalf("lifecycle events = %v", events)
		}
		if text != "echo: ping" {
			t.Fatalf("assistant text = %q, events = %v", text, events)
		}
	})

	t.Run("acp", func(t *testing.T) {
		server, err := newACPServer(agentRunner)
		if err != nil {
			t.Fatal(err)
		}
		client := &recordingClient{}
		conn, cleanup := connectACP(t, server, client)
		defer cleanup()

		ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
		defer cancel()
		initResp, err := conn.Initialize(ctx, acpsdk.InitializeRequest{
			ProtocolVersion: acpsdk.ProtocolVersionNumber,
		})
		if err != nil {
			t.Fatal(err)
		}
		if initResp.ProtocolVersion != acpsdk.ProtocolVersionNumber {
			t.Fatalf("protocol version %v", initResp.ProtocolVersion)
		}
		session, err := conn.NewSession(ctx, acpsdk.NewSessionRequest{
			Cwd:        t.TempDir(),
			McpServers: []acpsdk.McpServer{},
		})
		if err != nil {
			t.Fatal(err)
		}
		prompt, err := conn.Prompt(ctx, acpsdk.PromptRequest{
			SessionId: session.SessionId,
			Prompt:    []acpsdk.ContentBlock{acpsdk.TextBlock("ping")},
		})
		if err != nil {
			t.Fatal(err)
		}
		if prompt.StopReason != acpsdk.StopReasonEndTurn {
			t.Fatalf("stop reason %s", prompt.StopReason)
		}
		updates := client.updates()
		if len(updates) != 1 || updates[0] != "echo: ping" {
			t.Fatalf("session updates = %#v", updates)
		}
	})
}

func readAGUI(t *testing.T, body io.Reader) (events []string, text string) {
	t.Helper()
	scanner := bufio.NewScanner(body)
	for scanner.Scan() {
		line := strings.TrimSpace(scanner.Text())
		if !strings.HasPrefix(line, "data:") {
			continue
		}
		payload := strings.TrimSpace(strings.TrimPrefix(line, "data:"))
		var event struct {
			Type  string `json:"type"`
			Delta string `json:"delta"`
		}
		if err := json.Unmarshal([]byte(payload), &event); err != nil {
			t.Fatalf("event %s: %v", payload, err)
		}
		events = append(events, event.Type)
		if event.Type == "TEXT_MESSAGE_CONTENT" {
			text += event.Delta
		}
	}
	if err := scanner.Err(); err != nil {
		t.Fatal(err)
	}
	return events, text
}

func contains(items []string, want string) bool {
	for _, item := range items {
		if item == want {
			return true
		}
	}
	return false
}

type recordingClient struct {
	mu       sync.Mutex
	messages []string
}

func (c *recordingClient) SessionUpdate(_ context.Context, update acpsdk.SessionNotification) error {
	if update.Update.AgentMessageChunk != nil && update.Update.AgentMessageChunk.Content.Text != nil {
		c.mu.Lock()
		c.messages = append(c.messages, update.Update.AgentMessageChunk.Content.Text.Text)
		c.mu.Unlock()
	}
	return nil
}

func (c *recordingClient) updates() []string {
	c.mu.Lock()
	defer c.mu.Unlock()
	out := make([]string, len(c.messages))
	copy(out, c.messages)
	return out
}

func (*recordingClient) ReadTextFile(context.Context, acpsdk.ReadTextFileRequest) (acpsdk.ReadTextFileResponse, error) {
	return acpsdk.ReadTextFileResponse{}, errors.New("not implemented")
}

func (*recordingClient) WriteTextFile(context.Context, acpsdk.WriteTextFileRequest) (acpsdk.WriteTextFileResponse, error) {
	return acpsdk.WriteTextFileResponse{}, errors.New("not implemented")
}

func (*recordingClient) RequestPermission(context.Context, acpsdk.RequestPermissionRequest) (acpsdk.RequestPermissionResponse, error) {
	return acpsdk.RequestPermissionResponse{}, errors.New("not implemented")
}

func (*recordingClient) CreateTerminal(context.Context, acpsdk.CreateTerminalRequest) (acpsdk.CreateTerminalResponse, error) {
	return acpsdk.CreateTerminalResponse{}, errors.New("not implemented")
}

func (*recordingClient) KillTerminal(context.Context, acpsdk.KillTerminalRequest) (acpsdk.KillTerminalResponse, error) {
	return acpsdk.KillTerminalResponse{}, errors.New("not implemented")
}

func (*recordingClient) TerminalOutput(context.Context, acpsdk.TerminalOutputRequest) (acpsdk.TerminalOutputResponse, error) {
	return acpsdk.TerminalOutputResponse{}, errors.New("not implemented")
}

func (*recordingClient) ReleaseTerminal(context.Context, acpsdk.ReleaseTerminalRequest) (acpsdk.ReleaseTerminalResponse, error) {
	return acpsdk.ReleaseTerminalResponse{}, errors.New("not implemented")
}

func (*recordingClient) WaitForTerminalExit(context.Context, acpsdk.WaitForTerminalExitRequest) (acpsdk.WaitForTerminalExitResponse, error) {
	return acpsdk.WaitForTerminalExitResponse{}, errors.New("not implemented")
}

func connectACP(t *testing.T, server *acp.Server, client acpsdk.Client) (*acpsdk.ClientSideConnection, func()) {
	t.Helper()
	serverSide, clientSide := net.Pipe()
	serverConn, err := server.Connect(serverSide, serverSide)
	if err != nil {
		t.Fatal(err)
	}
	clientConn := acpsdk.NewClientSideConnection(client, clientSide, clientSide)
	return clientConn, func() {
		_ = clientSide.Close()
		select {
		case <-serverConn.Done():
		case <-time.After(time.Second):
			t.Error("ACP server connection did not close")
		}
	}
}
