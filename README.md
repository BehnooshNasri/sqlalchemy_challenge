# sqlalchemy_challenge
While defining the homepage for all the available routes, due to the route definitions in Flask app there was an error. Specifically, defining routes like "/api/v1.0/<start>" and "/api/v1.0/<start>/<end>", Flask expected those to be dynamic routes where <start> and <end> are placeholders for variable values and did not show "<start>" or "<start>/<end>" in the "Available Routes" list.

To fix this issue, the following solution from ChatGPT helped:
    "/api/v1.0/&lt;start&gt; (replace &lt;start&gt; with an actual start date)<br/>"
    "/api/v1.0/&lt;start&gt;/&lt;end&gt; (replace &lt;start&gt; and &lt;end&gt; with actual start and end dates)" 
