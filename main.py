from src.agent import build_graph


def main():
    app = build_graph()

    print(" Hybrid AI Agent Ready!")

    while True:
        query = input("\n Ask your question (or type 'exit'): ")

        if query.lower() == "exit":
            break

        result = app.invoke({"query": query})

        print("\n Answer:\n")
        print(result["final_answer"])


if __name__ == "__main__":
    main()