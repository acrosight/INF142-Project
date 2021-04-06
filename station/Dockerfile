# Builder stage
FROM python:3.8 AS builder
COPY requirements.txt .

# Install the required modules.
RUN pip install --user -r requirements.txt

# Publish stage
FROM python:3.8-slim AS publish
WORKDIR /code

# Copy the dependencies installed from the builder stage.
COPY --from=builder /root/.local /root/.local
COPY . .

# update PATH environment variable for pip packages
ENV PATH=/root/.local:$PATH


CMD ["python", "./station_client.py"]

