from Agent_related.graph import agent

def main():

    idea = input("Enter your startup idea: ")

    result = agent.invoke({
        "user_input": idea
    })

    report = result["final_report"]

    print("\n===== STARTUP VALIDATION REPORT =====\n")
    print(report)

    filename = "startup_report.md"
    with open(filename, "w", encoding="utf-8") as f:
        f.write("# Startup Validation Report\n\n")
        f.write(f"**Idea:** {idea}\n\n")
        f.write(report)
    print(f"\nReport saved to {filename}")


if __name__ == "__main__":
    main()
