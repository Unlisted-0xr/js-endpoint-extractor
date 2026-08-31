/* Simulated production-style JavaScript bundle.
   All domains/endpoints are fictional. */

(() => {
  "use strict";

  const CONFIG = {
    api: "https://api.demo.invalid",
    auth: "https://auth.demo.invalid",
    cdn: "https://cdn.demo.invalid"
  };

  const routes = {
    login: "/api/v1/auth/login",
    refresh: "/api/v1/auth/refresh",
    profile: "/api/v2/users/me",
    users: "/api/v2/users",
    search: "/api/v2/search?q=demo&page=1",
    orders: "/api/v2/orders?userId=42&status=open",
    upload: "/api/v1/files/upload",
    callback: "/oauth/callback",
    admin: "/internal/admin/settings",
    graphql: "/graphql",
    health: "/health"
  };

  const websocket = "wss://events.demo.invalid/socket";

  const files = [
    "/assets/app.js",
    "/assets/config.json",
    "/downloads/client.zip"
  ];

  const headers = {
    "Authorization": "Bearer <example>",
    "X-Client-Version": "1.4.2"
  };

  function request(path, options = {}) {
    return fetch(CONFIG.api + path, {
      ...options,
      headers: {
        ...headers,
        ...options.headers
      }
    });
  }

  async function getUser() {
    return request("/api/v2/users/me");
  }

  async function getOrder(id) {
    return request(`/api/v2/orders/${id}`);
  }

  function search(term, page = 1) {
    return request(
      "/api/v2/search?query=" +
      encodeURIComponent(term) +
      "&page=" +
      page
    );
  }

  function openEvents() {
    return new WebSocket(websocket);
  }

  const graphqlEndpoint = "/graphql";

  const telemetry =
    "https://telemetry.demo.invalid/v1/events";

  const documentation =
    "https://docs.demo.invalid/api";

  const redirectUrl =
    "/login?redirect=/dashboard&next=/home";

  const parameters = {
    userId: "42",
    accountId: "1001",
    tenant: "demo"
  };

  const moduleMap = {
    profile: "/api/v2/profile",
    settings: "/api/v2/account/settings",
    keys: "/api/v2/account/keys"
  };

  // Normal JavaScript noise:
  const noisy = {
    token: "example",
    pathname: "/x",
    getClient: true,
    constructor: "Object",
    DEBUG_BUILD: true
  };

  window.__APP_CONFIG__ = {
    apiBase: CONFIG.api,
    graphql: graphqlEndpoint,
    version: "2026.08"
  };
})();