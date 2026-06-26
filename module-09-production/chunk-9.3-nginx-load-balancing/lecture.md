*Full-Stack Web Dev · Module 9 — Production & Load Balancing*

# Chunk 9.3 — Nginx Reverse Proxy & Load Balancing

**📖 LECTURE** · **⏱️ 90–120 min**

> 📄 **Prefer the styled version?** Open [`lecture.html`](lecture.html) in your browser for the formatted page with colors and live demos.

---

## 🎯 What you'll learn

- What a **reverse proxy** is, and how it differs from a **load balancer** (and a forward proxy).
- Why you **scale out** (horizontal) instead of just up (vertical).
- How an Nginx **upstream** block distributes requests across multiple FastAPI replicas (**round-robin** and friends).
- Why **stateless JWT** auth lets you load-balance freely — and what **sticky sessions** are for when you can't.
- The **SQLite single-writer** problem that appears the moment you run multiple replicas, and when to move to Postgres.

In the lab you'll put Nginx in front of **2+ FastAPI replicas** and watch requests fan out across them.

## 1. Proxies, reverse proxies, load balancers

These terms overlap, so pin them down. They're all "a server in the middle," but facing different directions:

| Thing | Sits in front of | Job |
| --- | --- | --- |
| **Forward proxy** | The *clients* | Hides/controls users going out to the internet (e.g. a corporate proxy). |
| **Reverse proxy** | Your *servers* | One public front door; forwards incoming requests to backend services. |
| **Load balancer** | Your *servers* | A reverse proxy that spreads traffic across *multiple* identical backends. |

A **reverse proxy** is a single entry point that receives every request and decides where it goes. Even with one backend it's valuable: it terminates TLS (HTTPS), serves static files, sets headers, hides your internal topology, and gives the browser a single origin to talk to. You already used Nginx as a reverse-proxy-ish static server in 9.2.

A **load balancer** is a reverse proxy with more than one backend behind it, sharing the load. Nginx is both — flip on a few extra lines and your reverse proxy becomes a load balancer.

> **📝 One mental model**
>
> Think of a restaurant host. A
>
> reverse proxy
>
> is the host who greets everyone at the door and points them to the kitchen. A
>
> load balancer
>
> is that host when there are several identical kitchens — seating parties across them so no one kitchen is swamped.

## 2. Why scale out?

A single backend container can only do so much. When traffic grows you have two options:

- **Vertical scaling (up):** give the one server more CPU/RAM. Simple, but there's a ceiling, it's expensive at the top end, and that one server is a single point of failure.
- **Horizontal scaling (out):** run *more copies* of the server and share traffic among them. Near-unlimited headroom, and if one copy dies the others carry on.

Horizontal scaling is the production default — it's how you handle both **load** (more replicas = more throughput) and **resilience** (a dead replica is routed around). It's exactly why you containerized in 9.2: an image is trivially copyable, so running 2 or 20 replicas is just a number.

>

## 3. The Nginx `upstream` block

You tell Nginx about a pool of backends with an `upstream` block, then `proxy_pass` to that pool. Here's the heart of it:

```
upstream api_pool {
    server api1:8000;
    server api2:8000;
    server api3:8000;
}

server {
    listen 80;

    # Serve the built frontend...
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }

    # ...and forward API calls to the pool.
    location /api/ {
        proxy_pass http://api_pool/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

By default Nginx uses **round-robin**: request 1 → api1, request 2 → api2, request 3 → api3, request 4 → api1, and so on. Even, simple, effective. Those `proxy_set_header` lines pass the real client info through so your backend logs (8.1!) can still see who's calling instead of just "Nginx."

> **💡 Same origin, no more CORS headaches**
>
> Notice the browser now talks
>
> only
>
> to Nginx: the frontend at
>
> /
>
> and the API at
>
> /api/
>
> are the
>
> same origin
>
> . That sidesteps CORS entirely and means the frontend can use a relative
>
> VITE_API_URL=/api
>
> — no hardcoded host or port. This is the clean production layout.

## 4. Load-balancing strategies

Round-robin is the default, but Nginx offers others for when your backends aren't uniform or requests vary wildly in cost:

| Strategy | Directive | When to use |
| --- | --- | --- |
| **Round-robin** | (default) | Backends are identical & requests are similar. The sane default. |
| **Least connections** | `least_conn;` | Request durations vary a lot — send the next request to the least-busy replica. |
| **Weighted** | `server api1:8000 weight=3;` | Some replicas are bigger/faster — give them a larger share. |
| **IP hash** | `ip_hash;` | Pin each client IP to the same backend (a form of sticky sessions — see below). |

For the Tasks API, identical replicas + round-robin is exactly right.

## 5. Sticky sessions vs stateless JWT (the big idea)

Here's the question load balancing forces you to answer: **request 2 might land on a different replica than request 1. Will that break anything?**

It depends entirely on where your auth state lives — and this is where Module 7's design pays off enormously.

### The session approach (would need stickiness)

If you'd used server-side **sessions** (session data stored in *one* server's memory), then a user who logged in on api1 has their session only on api1. If round-robin sends their next request to api2, api2 has no idea who they are → logged out. The patch is **sticky sessions** (a.k.a. session affinity): the load balancer pins each user to the same backend (e.g. via `ip_hash` or a cookie). It works, but it undermines balancing (one replica can get overloaded) and breaks when that replica dies (those users lose their sessions).

### The JWT approach (no stickiness needed)

You used **stateless JWTs**. The token *itself* carries the user's identity and is signed with a `SECRET_KEY` that **every replica shares**. So *any* replica can verify *any* token with no lookup and no shared session store. Request 1 on api1, request 2 on api2, request 3 on api3 — all work identically. Your backends are **stateless**, so the load balancer can send each request anywhere. *This is why the course chose JWT back in 7.2.*

> **⚠️ One condition: every replica must share the same SECRET_KEY**
>
> Stateless auth across replicas only works if all replicas verify with the same signing secret. If api1 signs with one key and api2 has a different key, api2 rejects api1's tokens (401). In Compose, pass the
>
> same
>
> SECRET_KEY
>
> env var to every replica (you already do — one env, many containers).

|  | Server sessions | Stateless JWT (you) |
| --- | --- | --- |
| State lives | In one server's memory | In the token (client holds it) |
| Needs sticky sessions? | Yes | **No** |
| Replica dies | Its users get logged out | No impact — any replica serves them |
| Scales out cleanly | Awkward | Trivially |

## 6. Health checks & routing around dead replicas

What happens when a replica crashes? Nginx does **passive health checks** out of the box: if a backend fails or times out, Nginx marks it temporarily down and sends the request to another one — the user never notices. You can tune the thresholds:

```
upstream api_pool {
    server api1:8000 max_fails=3 fail_timeout=10s;
    server api2:8000 max_fails=3 fail_timeout=10s;
}
```

This is where your 8.2 `/health` endpoint earns its keep: Docker (and orchestrators like Kubernetes) call it to decide whether a replica is alive and should receive traffic. Cheap liveness checks + a load balancer that routes around failures = an app that stays up even when individual replicas don't.

## 7. The catch: SQLite and multiple writers

You scaled the *app* tier to N replicas. But they all talk to **one** database. The app is stateless; the data is not — and SQLite has a hard limit here.

**SQLite allows only one writer at a time.** It's a file, not a server. Multiple replicas sharing one SQLite file (via the volume from 9.2) can *read* concurrently just fine, but concurrent *writes* serialize, and under real load you'll see `database is locked` errors. Two mitigations help a little:

- **WAL mode** (`PRAGMA journal_mode=WAL`) lets readers and a writer coexist better — but still only one writer.
- A shared volume so every replica opens the *same* file (multiple separate files would be chaos).

These let you *demonstrate* load balancing for the lab, which is the goal. But they don't make SQLite a multi-writer database — it isn't one.

> **⚠️ The honest limit — when to move to Postgres**
>
> SQLite is superb for development, single-instance apps, and low write concurrency. The moment you genuinely scale out a write-heavy app, you've outgrown it. The fix is a real client/server database —
>
> PostgreSQL
>
> — which is built for many concurrent writers over the network. Thanks to SQLAlchemy, that migration is mostly changing
>
> DATABASE_URL
>
> and the driver; your models and queries barely change. We'll lay this out concretely in 9.4 (and the Bonus Track does it on GCP with Cloud SQL).

## 8. Seeing it work: which replica answered?

Round-robin is invisible unless you make it visible. The trick: have each replica reveal its identity. Inside a container, the hostname is the container id, so you can log it or return it in a header/field. If your backend reports `os.uname().nodename` (or `socket.gethostname()`), then repeated requests will show the value rotating across replicas — proof the load balancer is spreading the work. You'll add exactly this in the lab.

## ✅ Recap

- A **reverse proxy** is one front door for your servers; a **load balancer** is a reverse proxy spreading traffic across *multiple* identical backends.
- **Scale out** (more replicas) beats scaling up for throughput and resilience — easy because your app is a copyable image.
- Nginx's **upstream** + `proxy_pass` gives round-robin by default; `least_conn`/weights/`ip_hash` exist for special cases.
- **Stateless JWT** (with a shared `SECRET_KEY`) means any replica serves any request — **no sticky sessions** needed. That's why the course chose JWT.
- One database under many replicas exposes **SQLite's single-writer limit**; fine to demo, but real write-scaling means **moving to Postgres**.

**Next:** open `assignment.html` and build the load-balanced stack.

---

**Navigate:** **📖 Lecture** · [🧪 Assignment](assignment.md) · [✅ Solution](solution.md)
