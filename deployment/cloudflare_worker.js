// File: deployment/cloudflare_worker.js

export default {
  async fetch(request, env, ctx) {
    const { pathname } = new URL(request.url);

    if (pathname === "/checkout") {
      const requestData = await request.json();
      return new Response(
        JSON.stringify({
          message: "Checkout processed",
          payload: requestData,
          status: "success"
        }),
        { status: 200, headers: { "Content-Type": "application/json" } }
      );
    }

    if (pathname === "/cart") {
      return new Response(
        JSON.stringify({
          items: [
            { id: 1, name: "T-shirt", quantity: 2 },
            { id: 2, name: "Sneakers", quantity: 1 }
          ]
        }),
        { status: 200, headers: { "Content-Type": "application/json" } }
      );
    }

    if (pathname === "/telemetry") {
      return new Response(
        JSON.stringify({
          forecast: {
            expected_rps: 4670,
            recommendation: "scale_up"
          },
          timestamp: new Date().toISOString()
        }),
        { status: 200, headers: { "Content-Type": "application/json" } }
      );
    }

    return new Response(
      JSON.stringify({ error: "Endpoint not found" }),
      { status: 404, headers: { "Content-Type": "application/json" } }
    );
  }
};
