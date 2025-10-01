module.exports = {
  apps: [{
    name: "fastapi-api",
    script: "venv/bin/python3",
    args: "-m uvicorn main:app --host 0.0.0.0 --port 8000",


    env: {
      NODE_ENV: "production",
      DATABASE_URL: "postgresql+psycopg2://Andres:andr3sss06@bdd.crogaywqknnq.us-east-2.rds.amazonaws.com:5432/postgres"
    },
    autorestart: true,
    watch: false,
    max_memory_restart: '256M'
  }]
};