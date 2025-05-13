from prefect.agent import OrionAgent

if __name__ == "__main__":
    OrionAgent(work_queue="default").start()
