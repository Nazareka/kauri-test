# kauri-test

This is a repository for Kauri test task.

To run the application via docker compose, run the following command:

```sh
docker-compose up --build
```

The application will be accessible at `http://localhost:8000`.

Documentation for the API can be found at `http://localhost:8000/docs`.

Binance and Kraken were implemented as the exchange APIs.

Binance Credentials are actually not required to fetch prices. However, if you want to use the Binance API with credentials, 
you can set the `BINANCE_API_KEY` and `BINANCE_API_SECRET` environment variables in the `.env` file.