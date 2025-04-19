from flask import Flask, request
import time
import random

# Cloud Profiler setup
try:
    import googlecloudprofiler
    googlecloudprofiler.start(
        service='flask-demo',
        service_version='1.0.0'
    )
    print("Cloud Profiler started")
except Exception as e:
    print(f"Could not start profiler: {e}")

# Cloud Trace setup
from google.cloud import trace_v2
from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Initialize tracer and exporter
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
cloud_trace_exporter = CloudTraceSpanExporter()
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(cloud_trace_exporter))

# Flask app
app = Flask(__name__)

@app.route("/")
def index():
    with tracer.start_as_current_span("index-handler"):
        delay = random.uniform(0.1, 0.5)
        time.sleep(delay)  # simulate processing
        return f"Hello from Flask! (delay={delay:.2f}s)"

@app.route("/compute")
def compute():
    with tracer.start_as_current_span("compute-handler"):
        result = sum(i * i for i in range(100000))
        return f"Computation result: {result}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
