module.exports = {
  apps: [
    {
      name: "generador-frontend",
      script: "npm",
      args: "run start",
      cwd: "./frontend",
      env: {
        NODE_ENV: "production",
        PORT: 3000
      }
    },
    {
      name: "generador-backend",
      script: "./venv/bin/uvicorn",
      args: "main:app --host 0.0.0.0 --port 8000",
      interpreter: "./venv/bin/python",
      cwd: ".",
      env: {
        PYTHONUNBUFFERED: "1"
      }
    }
  ]
};
