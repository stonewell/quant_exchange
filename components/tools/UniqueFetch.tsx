const ABORT_REQUEST_CONTROLLERS = new Map();

export async function uniqueFetch(
  url: any,
  {
    signalKey, // Must be unique. If provided, the request will be abortable.
    ...rest
  } = {}
) {
  return await fetch(url, {
    ...(signalKey && { signal: abortAndGetSignalSafe(signalKey) }),
    ...rest
  }).catch(error => {
    if (error == 'CANCELLED') {
      return new Response(JSON.stringify([]), {
        status: 418, // Cancelled
        statusText: error.message || 'Client Cancel',
      })
    }
    if (error.name === 'AbortError') {
      return new Response(JSON.stringify([]), {
        status: 499, // Client Closed Request
        statusText: error.message || 'Client Closed Request',
      })
    } return new Response(JSON.stringify([]), {
      status: 599, // Network Connect Timeout Error
      statusText: error.message || 'Network Connect Timeout Error',
    })
  });
}

export function abortRequestSafe(key, reason = "CANCELLED") {
  ABORT_REQUEST_CONTROLLERS.get(key)?.abort?.(reason);
}

function abortAndGetSignalSafe(key) {
  abortRequestSafe(key); // abort previous request, if any
  const newController = new AbortController();
  ABORT_REQUEST_CONTROLLERS.set(key, newController);
  return newController.signal;
}
