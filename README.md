PROJECT 4: Web Crawler
Partners: Tymofii Kryvtsun, Carter Codell

We've created a web crawler to crawl the Fakebook website,
and extract secret keys hidden in the random locations.
We've created HTTPRequest class to construct a valid http request,
HTTP class to send the request to the server using sockets, and the Crawler to manage
all requests.

Our Crawler starts by logging user in and extracting cookies.Then it parses pages one by one,
extracting all profile links from the page and adding them to the queue. It keeps
track of already visited links not to get into the loop.

Problems: The biggest problem we had was not getting any response form the server for HTTP/1.1
(sometimes it stopped responding and did not react on our reconnection attempts).
Therefore for HTTP/1.1 we create a new socket for each request. It slowed down the process a lot.

Libraries: html.parser