package main

import (
	"context"
	"fmt"
	"math"

	"github.com/google/uuid"

	"trpc.group/trpc-go/trpc-agent-go/agent"
	"trpc.group/trpc-go/trpc-agent-go/agent/llmagent"
	"trpc.group/trpc-go/trpc-agent-go/event"
	"trpc.group/trpc-go/trpc-agent-go/model"
	"trpc.group/trpc-go/trpc-agent-go/model/openai"
	"trpc.group/trpc-go/trpc-agent-go/tool"
	"trpc.group/trpc-go/trpc-agent-go/tool/function"
)

const agentName = "dual-assistant"

// newAgent builds the agent shared by ACP and AG-UI.
// kind "echo" answers without a model so the protocols can be exercised locally.
// kind "llm" is an OpenAI-compatible LLMAgent; it reads OPENAI_API_KEY and
// the optional OPENAI_BASE_URL.
func newAgent(kind, modelName string, stream bool) (agent.Agent, error) {
	switch kind {
	case "echo":
		return &echoAgent{name: agentName}, nil
	case "llm":
		if modelName == "" {
			return nil, fmt.Errorf("model name is required for -agent llm")
		}
		return newLLMAgent(modelName, stream), nil
	default:
		return nil, fmt.Errorf("unknown agent kind %q (want echo or llm)", kind)
	}
}

func newLLMAgent(modelName string, stream bool) agent.Agent {
	calculatorTool := function.NewFunctionTool(
		calculator,
		function.WithName("calculator"),
		function.WithDescription("Add, subtract, multiply, divide, or raise to a power."),
	)
	generation := model.GenerationConfig{
		MaxTokens:   intPtr(512),
		Temperature: floatPtr(0.7),
		Stream:      stream,
	}
	return llmagent.New(
		agentName,
		llmagent.WithModel(openai.New(modelName)),
		llmagent.WithTools([]tool.Tool{calculatorTool}),
		llmagent.WithGenerationConfig(generation),
		llmagent.WithDescription("Assistant exposed through ACP and AG-UI."),
		llmagent.WithInstruction("You are a concise assistant. Use the calculator tool for arithmetic."),
	)
}

type echoAgent struct {
	name string
}

func (a *echoAgent) Run(ctx context.Context, invocation *agent.Invocation) (<-chan *event.Event, error) {
	text := "echo: " + invocation.Message.Content
	response := &model.Response{
		ID:     uuid.NewString(),
		Object: model.ObjectTypeChatCompletion,
		Done:   true,
		Choices: []model.Choice{{
			Message: model.Message{
				Role:    model.RoleAssistant,
				Content: text,
			},
		}},
	}
	events := make(chan *event.Event, 1)
	go func() {
		defer close(events)
		_ = event.EmitEvent(ctx, events, event.NewResponseEvent(
			invocation.InvocationID,
			a.name,
			response,
		))
	}()
	return events, nil
}

func (a *echoAgent) Tools() []tool.Tool { return nil }

func (a *echoAgent) Info() agent.Info {
	return agent.Info{
		Name:        a.name,
		Description: "Deterministic assistant used to exercise ACP and AG-UI.",
	}
}

func (a *echoAgent) SubAgents() []agent.Agent { return nil }

func (a *echoAgent) FindSubAgent(string) agent.Agent { return nil }

func calculator(_ context.Context, args calculatorArgs) (calculatorResult, error) {
	var result float64
	switch args.Operation {
	case "add", "+":
		result = args.A + args.B
	case "subtract", "-":
		result = args.A - args.B
	case "multiply", "*":
		result = args.A * args.B
	case "divide", "/":
		if args.B == 0 {
			return calculatorResult{}, fmt.Errorf("division by zero")
		}
		result = args.A / args.B
	case "power", "^":
		result = math.Pow(args.A, args.B)
	default:
		return calculatorResult{}, fmt.Errorf("invalid operation: %s", args.Operation)
	}
	return calculatorResult{Result: result}, nil
}

type calculatorArgs struct {
	Operation string  `json:"operation" description:"add, subtract, multiply, divide, power"`
	A         float64 `json:"a" description:"First number"`
	B         float64 `json:"b" description:"Second number"`
}

type calculatorResult struct {
	Result float64 `json:"result"`
}

func intPtr(v int) *int { return &v }

func floatPtr(v float64) *float64 { return &v }
