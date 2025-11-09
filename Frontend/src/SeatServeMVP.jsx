import { useMemo, useState, useEffect } from "react";

// --- Speedee Burgers Catalog ---
const CATALOG = [
  { id: "p1", name: "Classic Burger", price: 10.0, category: "Food", station: "Grill", image: "/Images/classic-burger.png" },
  { id: "p2", name: "Cheese Burger", price: 11.0, category: "Food", station: "Grill", image: "/Images/cheese-burger.png" },
  { id: "p3", name: "Chicken Tenders", price: 9.0, category: "Food", station: "Fry", image: "/Images/chicken-tenders.png" },
  { id: "p4", name: "Soda Small 16oz", price: 2.5, category: "Drinks", station: "Beverage", image: "/Images/soda-small-16oz.png" },
  { id: "p5", name: "Soda Medium 21oz", price: 3.0, category: "Drinks", station: "Beverage", image: "/Images/soda-medium-21oz.png" },
  { id: "p6", name: "Soda Large 32oz", price: 3.5, category: "Drinks", station: "Beverage", image: "/Images/soda-large-32oz.png" },
  { id: "p7", name: "Bottled Water", price: 2.5, category: "Drinks", station: "Beverage", image: "/Images/bottled-water.png" },
  { id: "p8", name: "Milkshake", price: 5.0, category: "Drinks", station: "Dessert", image: "/Images/milkshake.png" },
];

const CATEGORIES = ["All", ...Array.from(new Set(CATALOG.map((i) => i.category)))];
const STATIONS = ["All", ...Array.from(new Set(CATALOG.map((i) => i.station)))];

function classNames(...xs) {
  return xs.filter(Boolean).join(" ");
}

function currency(n) {
  return new Intl.NumberFormat(undefined, { style: "currency", currency: "USD" }).format(n);
}

const STATUS_FLOW = ["Queued", "Preparing", "Ready", "Delivered"];

export default function SeatServeMVP() {
  const [tab, setTab] = useState("Menu Items"); // "Menu Items" | "Order Status"
  const [user, setUser] = useState(() => {
    return localStorage.getItem('seatserve_user') || 'Guest User';
  });

  // Fan state
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("All");
  const [station, setStation] = useState("All");
  const [cart, setCart] = useState({}); // id -> qty
  const [fulfillment, setFulfillment] = useState("Pickup"); // "Pickup" | "Seat Delivery"
  const [seatSection, setSeatSection] = useState("");
  const [seatRow, setSeatRow] = useState("");
  const [seatNumber, setSeatNumber] = useState("");
  const [note, setNote] = useState("");

  // Shared orders list (persisted in localStorage)
  const [orders, setOrders] = useState(() => {
    const savedOrders = localStorage.getItem('seatserve_orders');
    return savedOrders ? JSON.parse(savedOrders) : [];
  });

  // ---- Dev Smoke Tests (run once in dev) ----
  useEffect(() => {
    const DEV = typeof import.meta !== "undefined" && import.meta.env && import.meta.env.DEV;
    if (!DEV) return;
    try {
      console.log("[SeatServe] Running smoke tests...");
      // Currency sanity
      const c = currency(12.34);
      console.assert(typeof c === "string" && /12/.test(c), "currency() should return a string containing the numeric value");
      // Status flow monotonic
      let s = "Queued";
      const seq = [s];
      for (let i = 0; i < 3; i++) {
        const idx = STATUS_FLOW.indexOf(s);
        s = STATUS_FLOW[Math.min(idx + 1, STATUS_FLOW.length - 1)];
        seq.push(s);
      }
      console.assert(seq[0] === "Queued" && seq.at(-1) === "Delivered", "Status should advance to Delivered in <=3 steps");
      console.log("[SeatServe] Smoke tests passed ✓");
    } catch (e) {
      console.warn("[SeatServe] Smoke tests failed:", e);
    }
  }, []);

  // Persist orders to localStorage whenever they change
  useEffect(() => {
    localStorage.setItem('seatserve_orders', JSON.stringify(orders));
  }, [orders]);

  // Check for flag to switch to order status tab (from confirmation page)
  useEffect(() => {
    if (localStorage.getItem('switch_to_concession') === 'true') {
      setTab('Order Status');
      localStorage.removeItem('switch_to_concession');
    }
  }, []);

  // Auto-advance order status for demo purposes
  useEffect(() => {
    if (tab === 'Order Status' && orders.length > 0) {
      const interval = setInterval(() => {
        setOrders((prev) => 
          prev.map((order) => {
            if (order.status === 'Delivered') return order;
            
            const currentIndex = STATUS_FLOW.indexOf(order.status);
            const nextIndex = Math.min(currentIndex + 1, STATUS_FLOW.length - 1);
            return { ...order, status: STATUS_FLOW[nextIndex] };
          })
        );
      }, 15000); // Advance every 15 seconds
      
      return () => clearInterval(interval);
    }
  }, [tab, orders.length]);

  const filtered = useMemo(() => {
    const q = search.trim().toLowerCase();
    return CATALOG.filter((item) => {
      const okCat = category === "All" || item.category === category;
      const okStation = station === "All" || item.station === station;
      const okSearch = !q || item.name.toLowerCase().includes(q);
      return okCat && okStation && okSearch;
    });
  }, [search, category, station]);

  const cartEntries = Object.entries(cart);
  const cartTotal = cartEntries.reduce((sum, [id, qty]) => {
    const item = CATALOG.find((i) => i.id === id);
    return sum + (item ? item.price * qty : 0);
  }, 0);

  function addToCart(id) {
    setCart((prev) => ({ ...prev, [id]: (prev[id] || 0) + 1 }));
  }
  function decFromCart(id) {
    setCart((prev) => {
      const next = { ...prev };
      if (!next[id]) return prev;
      next[id] -= 1;
      if (next[id] <= 0) delete next[id];
      return next;
    });
  }
  function clearCart() {
    setCart({});
  }

  function placeOrder() {
    if (!cartEntries.length) return;
    if (fulfillment === "Seat Delivery" && (!seatSection.trim() || !seatRow.trim() || !seatNumber.trim())) {
      return alert("Please enter your complete seat location (Section, Row, and Seat).");
    }

    const snapshot = cartEntries.map(([id, qty]) => {
      const item = CATALOG.find((i) => i.id === id);
      return { id, name: item?.name || id, price: item?.price || 0, qty };
    });

    const seatLocation = fulfillment === "Seat Delivery" 
      ? `Section ${seatSection.trim()}, Row ${seatRow.trim()}, Seat ${seatNumber.trim()}`
      : null;

    const newOrder = {
      id: `ORD-${Math.random().toString(36).slice(2, 8).toUpperCase()}`,
      items: snapshot,
      total: snapshot.reduce((s, it) => s + it.price * it.qty, 0),
      fulfillment,
      seat: seatLocation,
      note: note.trim() || null,
      status: "Queued",
      concession: "Speedee Burgers",
      createdAt: new Date().toISOString(),
    };

    // Store order as pending and redirect to checkout
    localStorage.setItem('pending_order', JSON.stringify(newOrder));
    setOrders((prev) => [newOrder, ...prev]);
    clearCart();
    setNote("");
    if (fulfillment === "Seat Delivery") {
      setSeatSection("");
      setSeatRow("");
      setSeatNumber("");
    }
    
    // Redirect to checkout page
    window.location.href = '/checkout.html';
  }

  function advanceStatus(orderId) {
    setOrders((prev) =>
      prev.map((o) => {
        if (o.id !== orderId) return o;
        const idx = STATUS_FLOW.indexOf(o.status);
        const nextStatus = STATUS_FLOW[Math.min(idx + 1, STATUS_FLOW.length - 1)];
        return { ...o, status: nextStatus };
      })
    );
  }

  function cancelOrder(orderId) {
    setOrders((prev) => prev.filter((o) => o.id !== orderId));
  }

  function logout() {
    localStorage.removeItem('seatserve_logged_in');
    localStorage.removeItem('seatserve_user');
    window.location.href = '/';
  }

  return (
    <div className="min-h-screen bg-white text-neutral-900 relative">
      {/* Speedee Burgers Logo Wallpaper */}
      <div 
        className="fixed inset-0 pointer-events-none opacity-25"
        style={{
          backgroundImage: 'url(/Images/speedee-burgers-logo.png)',
          backgroundRepeat: 'no-repeat',
          backgroundPosition: 'center',
          backgroundSize: 'min(70vw, 70vh)',
          zIndex: 1
        }}
      />
      {/* Header */}
      <header className="sticky top-0 z-20 backdrop-blur bg-white/70 border-b border-neutral-300">
        <div className="mx-auto max-w-6xl px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="h-12 w-12 rounded-2xl overflow-hidden">
              <img src="/Images/seatserve-app-icon.png" alt="SeatServe Logo" className="w-full h-full object-cover" />
            </div>
            <div>
              <div className="text-xl font-semibold">SeatServe</div>
              <div className="text-xs text-neutral-500">Order from your seat or pick up fast</div>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <nav className="flex items-center gap-2 p-1 bg-blue-100 rounded-xl border border-neutral-300">
              {["Menu Items", "Order Status"].map((t) => (
                <button
                  key={t}
                  onClick={() => setTab(t)}
                  className={
                    classNames(
                      "px-3 py-1.5 rounded-lg text-sm transition",
                      tab === t ? "bg-emerald-300 text-neutral-900" : "text-neutral-600 hover:bg-neutral-200"
                    )
                  }
                  aria-pressed={tab === t}
                >
                  {t}
                </button>
              ))}
            </nav>
            
            <div className="flex items-center gap-2">
              <div className="text-sm text-neutral-600">
                Welcome, <span className="font-medium">{user}</span>
              </div>
              <button
                onClick={() => window.location.href = '/concessions.html'}
                className="px-3 py-1.5 rounded-lg text-sm bg-emerald-300 text-neutral-900 border border-emerald-300 hover:bg-emerald-400 hover:border-emerald-400 transition"
              >
                Change Store
              </button>
              <button
                onClick={logout}
                className="px-3 py-1.5 rounded-lg text-sm bg-emerald-300 text-neutral-900 border border-emerald-300 hover:bg-emerald-400 hover:border-emerald-400 transition"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-6xl px-4 py-6 grid gap-6 relative z-10">
        {tab === "Menu Items" ? (
          <section className="grid md:grid-cols-3 gap-6">
            {/* Left: Filters */}
            <aside className="md:col-span-1 space-y-4">
              <div className="p-4 rounded-2xl bg-blue-100 border border-neutral-300">
                <h2 className="font-semibold mb-3">Browse Menu</h2>
                <input
                  type="text"
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                  placeholder="Search items..."
                  className="w-full rounded-xl bg-white border border-neutral-300 px-3 py-2 outline-none focus:ring-2 focus:ring-emerald-400"
                />
                <div className="mt-3 grid grid-cols-2 gap-2">
                  <select
                    value={category}
                    onChange={(e) => setCategory(e.target.value)}
                    className="rounded-xl bg-white border border-neutral-300 px-3 py-2"
                    aria-label="Filter by category"
                  >
                    {CATEGORIES.map((c) => (
                      <option key={c} value={c}>{c}</option>
                    ))}
                  </select>
                  <select
                    value={station}
                    onChange={(e) => setStation(e.target.value)}
                    className="rounded-xl bg-white border border-neutral-300 px-3 py-2"
                    aria-label="Filter by station"
                  >
                    {STATIONS.map((s) => (
                      <option key={s} value={s}>{s}</option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="p-4 rounded-2xl bg-blue-100 border border-neutral-300">
                <h2 className="font-semibold mb-3">Fulfillment</h2>
                <div className="flex gap-2">
                  {["Pickup", "Seat Delivery"].map((f) => (
                    <button
                      key={f}
                      onClick={() => setFulfillment(f)}
                      className={classNames(
                        "px-3 py-1.5 rounded-lg text-sm border transition",
                        fulfillment === f
                          ? "bg-emerald-300 text-neutral-900 border-emerald-300"
                          : "bg-white text-neutral-700 border-neutral-300 hover:border-neutral-500"
                      )}
                      aria-pressed={fulfillment === f}
                    >
                      {f}
                    </button>
                  ))}
                </div>
                {fulfillment === "Seat Delivery" && (
                  <div className="mt-3 space-y-3">
                    <div>
                      <label className="text-sm text-neutral-700 mb-1 block">Section</label>
                      <input
                        type="text"
                        value={seatSection}
                        onChange={(e) => setSeatSection(e.target.value)}
                        placeholder="104"
                        className="w-full rounded-xl bg-white border border-neutral-300 px-3 py-2"
                      />
                    </div>
                    <div>
                      <label className="text-sm text-neutral-700 mb-1 block">Row</label>
                      <input
                        type="text"
                        value={seatRow}
                        onChange={(e) => setSeatRow(e.target.value)}
                        placeholder="F"
                        className="w-full rounded-xl bg-white border border-neutral-300 px-3 py-2"
                      />
                    </div>
                    <div>
                      <label className="text-sm text-neutral-700 mb-1 block">Seat</label>
                      <input
                        type="text"
                        value={seatNumber}
                        onChange={(e) => setSeatNumber(e.target.value)}
                        placeholder="12"
                        className="w-full rounded-xl bg-white border border-neutral-300 px-3 py-2"
                      />
                    </div>
                  </div>
                )}
              </div>
            </aside>

            {/* Middle: Catalog */}
            <section className="md:col-span-2 space-y-4">
              <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {filtered.map((item) => (
                  <div key={item.id} className="rounded-2xl border border-neutral-300 bg-white overflow-hidden flex flex-col hover:shadow-lg hover:scale-105 transition-all duration-200 cursor-pointer">
                    <div className="h-28 bg-gradient-to-br from-neutral-100 to-neutral-200 flex items-center justify-center overflow-hidden">
                      {item.image ? (
                        <img src={item.image} alt={item.name} className="w-full h-full object-cover" />
                      ) : null}
                    </div>
                    <div className="p-4 flex-1 flex flex-col">
                      <div className="flex items-center justify-between mb-1">
                        <h3 className="font-semibold tracking-tight">{item.name}</h3>
                        <div className="text-sm text-neutral-600">{currency(item.price)}</div>
                      </div>
                      <div className="text-xs text-neutral-500">{item.category} • {item.station}</div>
                      <div className="mt-auto pt-3 flex items-center gap-2">
                        {cart[item.id] ? (
                          <div className="inline-flex items-center gap-2">
                            <button
                              onClick={() => decFromCart(item.id)}
                              className="h-8 w-8 rounded-lg border border-neutral-300 hover:border-neutral-500"
                              aria-label={`Decrease ${item.name}`}
                            >−</button>
                            <span className="min-w-6 text-center">{cart[item.id]}</span>
                            <button
                              onClick={() => addToCart(item.id)}
                              className="h-8 w-8 rounded-lg border border-neutral-300 hover:border-neutral-500"
                              aria-label={`Increase ${item.name}`}
                            >＋</button>
                          </div>
                        ) : (
                          <button
                            onClick={() => addToCart(item.id)}
                            className="ml-auto px-3 py-1.5 rounded-lg bg-emerald-400 text-neutral-900 font-medium hover:brightness-95"
                            aria-label={`Add ${item.name} to cart`}
                          >Add</button>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </section>

            {/* Right: Cart (on mobile, moves below) */}
            <section className="md:col-span-3 lg:col-span-3 xl:col-span-3">
              <div className="mt-2 p-4 rounded-2xl bg-blue-100 border border-neutral-300">
                <h2 className="font-semibold mb-3">Your Cart</h2>
                {cartEntries.length === 0 ? (
                  <p className="text-sm text-neutral-500">No items yet. Add something tasty!</p>
                ) : (
                  <div className="space-y-2">
                    {cartEntries.map(([id, qty]) => {
                      const item = CATALOG.find((i) => i.id === id) || { name: "", price: 0 };
                      return (
                        <div key={id} className="flex items-center justify-between text-sm">
                          <div className="flex items-center gap-2">
                            <div className="text-neutral-700 w-36 truncate" title={item.name}>{item.name}</div>
                            <div className="text-neutral-500">× {qty}</div>
                          </div>
                          <div className="flex items-center gap-2">
                            <div className="font-medium">{currency(item.price * qty)}</div>
                            <button
                              onClick={() => decFromCart(id)}
                              className="h-7 w-7 rounded-lg border border-neutral-300 hover:border-neutral-500"
                              aria-label={`Decrease ${item.name}`}
                            >−</button>
                            <button
                              onClick={() => addToCart(id)}
                              className="h-7 w-7 rounded-lg border border-neutral-300 hover:border-neutral-500"
                              aria-label={`Increase ${item.name}`}
                            >＋</button>
                          </div>
                        </div>
                      );
                    })}

                    <textarea
                      placeholder="Add a note (no onions, extra napkins, etc.)"
                      value={note}
                      onChange={(e) => setNote(e.target.value)}
                      className="w-full rounded-xl bg-white border border-neutral-300 px-3 py-2 text-sm mt-2"
                    />

                    <div className="flex items-center justify-between pt-2 border-t border-neutral-300">
                      <div className="text-neutral-600">Total</div>
                      <div className="text-lg font-semibold">{currency(cartTotal)}</div>
                    </div>

                    <div className="flex items-center gap-2">
                      <button
                        onClick={placeOrder}
                        className="px-4 py-3 rounded-xl bg-gradient-to-r from-emerald-400 to-cyan-400 text-neutral-900 font-semibold hover:from-emerald-500 hover:to-cyan-500 focus:ring-2 focus:ring-emerald-400 focus:ring-offset-2 transition duration-200"
                      >Checkout</button>
                      <button
                        onClick={clearCart}
                        className="px-4 py-2 rounded-xl border border-neutral-300 hover:border-neutral-500"
                      >Clear</button>
                    </div>
                  </div>
                )}
              </div>
            </section>
          </section>
        ) : (
          // Order Status Tab
          <section className="grid md:grid-cols-3 gap-6 relative">
            {/* Index Wallpaper Background for Order Status */}
            <div 
              className="absolute inset-0 pointer-events-none opacity-30 rounded-2xl overflow-hidden"
              style={{
                backgroundImage: 'url(/Images/index-wallpaper.png)',
                backgroundRepeat: 'no-repeat',
                backgroundPosition: 'center',
                backgroundSize: 'cover',
                zIndex: 1
              }}
            />
            <div className="md:col-span-3 relative z-10">
              <div className="p-4 rounded-2xl bg-blue-100 border border-neutral-300 shadow-lg">
                <div className="flex items-center justify-between mb-2">
                  <h2 className="font-semibold">Your Orders</h2>
                  <div className="text-xs text-neutral-500">{orders.length} order{orders.length !== 1 ? 's' : ''}</div>
                </div>
                {orders.length === 0 ? (
                  <p className="text-sm text-neutral-500">No orders yet. Switch to Menu Items to place your first order!</p>
                ) : (
                  <ul className="space-y-3">
                    {orders.map((o) => (
                      <li key={o.id} className="rounded-xl border border-neutral-300 bg-white p-3">
                        <div className="flex items-center justify-between gap-2">
                          <div className="flex items-center gap-3">
                            <span className="inline-flex items-center px-2 py-0.5 text-xs rounded-lg border border-neutral-300 text-neutral-700">
                              {o.id}
                            </span>
                            <span className="text-sm text-neutral-500">{new Date(o.createdAt).toLocaleTimeString()}</span>
                          </div>
                          <div className="text-sm">
                            <span
                              className={classNames(
                                "px-2 py-0.5 rounded-lg",
                                o.status === "Queued" && "bg-neutral-200",
                                o.status === "Preparing" && "bg-yellow-200 text-neutral-900",
                                o.status === "Ready" && "bg-emerald-300 text-neutral-900",
                                o.status === "Delivered" && "bg-neutral-400 text-neutral-900"
                              )}
                            >
                              {o.status}
                            </span>
                          </div>
                        </div>
                        <div className="mt-2 text-sm text-neutral-800">
                          {o.items.map((it) => (
                            <div key={it.id} className="flex items-center justify-between">
                              <div className="text-neutral-700">
                                {it.name} <span className="text-neutral-500">× {it.qty}</span>
                              </div>
                              <div>{currency(it.price * it.qty)}</div>
                            </div>
                          ))}
                          <div className="flex items-center justify-between mt-2 border-t border-neutral-200 pt-2">
                            <div className="text-neutral-600">
                              {o.fulfillment === "Pickup" ? "Pickup at counter" : `Deliver to seat: ${o.seat}`}
                              {o.note ? <span className="ml-2 text-neutral-500 italic">• {o.note}</span> : null}
                            </div>
                            <div className="font-semibold">{currency(o.total)}</div>
                          </div>
                        </div>
                        <div className="mt-3 flex items-center gap-2">
                          <div className="text-xs text-neutral-500">
                            {o.status === 'Queued' && '⏳ Your order is in the queue'}
                            {o.status === 'Preparing' && '👨‍🍳 Being prepared now'}
                            {o.status === 'Ready' && '✅ Ready for pickup!'}
                            {o.status === 'Delivered' && '🎉 Order completed'}
                          </div>
                        </div>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </div>
          </section>
        )}
      </main>

      <footer className="mx-auto max-w-6xl px-4 pb-10 pt-4 text-xs text-neutral-500">
        <div>Demo MVP | SeatServe All Rights Reserve 2025</div>
      </footer>
    </div>
  );
}