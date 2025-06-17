function handler(event) {
  var request = event.request;
  var host = request.headers.host.value

  if (!host.startsWith("www."))
    return {
      headers: {
        location: {
          value: "https://www." + host + request.uri
        }
      },
      statusCode: 301,
      statusDescription: "Moved Permanently"
    };

  if (request.uri.endsWith("/")) {
    request.uri += "index.html";
    return request;
  }

  if (request.uri.lastIndexOf(".") < request.uri.lastIndexOf("/")) {
    request.uri += "/index.html";
    return request;
  }

  return request;
}
