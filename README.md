# Socket Programming

## Iterative Server
> Port: 12345

This server handles connection requests one by one. If there is a connected client, other requests need to wait in queue until server is free.  
Server has queue size of 5, "Connection reset by peer" is thrown by client if the queue is already full.

```
python IterativeServer.py
python MultiThreadClient.py
```

## Concurrent Server
> Port: 12346

This server uses threads to serve connection requests. Client should be able to connect to server immediately regardless of number of connected clients.

```
python ConcurrentServer.py
python SingleClient.py
```
\* `MultiThreadClient.py` cannot display the input prompt for different clients at the same time
