# This module deploys the training flow so it can be retrained on a regular schedule.

from main import train_model_flow

if __name__ == "__main__":
    train_model_flow.serve(
        name="abalone-retrain",
        cron="0 2 * * *",  # every day at 02:00 -- adjust to your needs
    )
