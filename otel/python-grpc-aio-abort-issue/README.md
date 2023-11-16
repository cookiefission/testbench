# OTEL Python gRPC AIO abort issue

This is a replication for an issue with the OTEL Python library for
instrumenting grpc.aio. When calling `context.abort` with trailing metadata,
instrumented servicers raise a TypeError because the OTEL AIO server interceptor
is based on the plain grpc.ServicerContext, not the correct
grpc.aio.ServicerContext.

## Replication

```
# Set up
$ make env deps

$ python server.py

# In a separate terminal, this is the expected behaviour with unmasked abort exceptions
$ python client.py

Greeter client received: Hello, you!
UNKNOWN:Error received from peer  {created_time:"2023-11-16T14:41:55.097202+00:00", grpc_status:10, grpc_message:"This is the actual error message"}
UNKNOWN:Error received from peer  {grpc_message:"This is the actual error message", grpc_status:10, created_time:"2023-11-16T14:41:55.099292+00:00"}

# Restart server with OTEL instrumentation
$ opentelemetry-instrument --traces_exporter=console python server.py

# In a separate terminal, this shows the bug. Should be same as previous but raises TypeError
$ python client.py

Greeter client received: Hello, you!
UNKNOWN:Error received from peer  {grpc_message:"This is the actual error message", grpc_status:10, created_time:"2023-11-16T14:41:41.065518+00:00"}
UNKNOWN:Error received from peer  {created_time:"2023-11-16T14:41:41.067851+00:00", grpc_status:2, grpc_message:"Unexpected <class \'TypeError\'>: _OpenTelemetryServicerContext.abort() got an unexpected keyword argument \'trailing_metadata\'"}
```

### Minimal Replication

Swap `server.py` for `minimal_server.py` above. It only does the buggy case.
