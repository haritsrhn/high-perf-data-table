"use client";

import React, { useState } from "react";
import useSWR from "swr";
import { useVirtual } from "react-virtual";
import { fetcher } from "../lib/fetcher";

type Product = {
  id: number;
  name: string;
  description: string;
  price: number;
  category: string;
};

export default function ProductTable() {
  const [q, setQ] = useState("");
  const [category, setCategory] = useState("");
  const [sortBy, setSortBy] = useState("id");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("asc");
  const [page, setPage] = useState(1);

  const query = new URLSearchParams({
    q,
    category,
    sort_by: sortBy,
    sort_order: sortOrder,
    page: String(page),
    limit: "10",
  }).toString();

  const { data } = useSWR<Product[]>(
    `http://localhost:8000/products?${query}`,
    fetcher
  );

  const parentRef = React.useRef<HTMLDivElement>(null);
  const rowVirtualizer = useVirtual({
    parentRef,
    size: data?.length || 0,
    overscan: 20,
  });

  return (
    <div>
      {/* Filter and Sort Controls */}
      <div style={{ display: "flex", gap: "1rem", marginBottom: "1rem" }}>
        <input
          placeholder="Search..."
          value={q}
          onChange={(e) => setQ(e.target.value)}
        />
        <input
          placeholder="Category..."
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        />
        <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
          <option value="id">ID</option>
          <option value="name">Name</option>
          <option value="price">Price</option>
        </select>
        <select
          value={sortOrder}
          onChange={(e) => setSortOrder(e.target.value as "asc" | "desc")}
        >
          <option value="asc">Asc</option>
          <option value="desc">Desc</option>
        </select>
        <button onClick={() => setPage((p) => Math.max(p - 1, 1))}>Prev</button>
        <button onClick={() => setPage((p) => p + 1)}>Next</button>
      </div>

      {/* Virtualized Table */}
      <div ref={parentRef} style={{ height: "500px", overflow: "auto" }}>
        <div
          style={{
            height: `${rowVirtualizer.totalSize}px`,
            position: "relative",
          }}
        >
          {rowVirtualizer.virtualItems.map((virtualRow) => {
            const product = data?.[virtualRow.index];
            if (!product) return null;
            return (
              <div
                key={product.id}
                // onClick={() => window.location.href = `/product/${product.id}`}
                style={{
                  position: "absolute",
                  height: `${virtualRow.size}px`,
                  transform: `translateY(${virtualRow.start}px)`,
                  display: "flex",
                  alignItems: "center",
                  backgroundColor: "#fff",
                  border: "1px solid #ddd",
                  boxShadow: "0 1px 2px rgba(0, 0, 0, 0.1)",
                  marginBottom: "1px",
                  padding: "10px",
                  fontSize: "14px",
                  color: "#333",
                  fontFamily: "Arial, sans-serif",
                  fontWeight: "normal",
                  textDecoration: "none",
                  transition: "background-color 0.2s",
                  cursor: "pointer",
                  zIndex: 1,
                  borderBottom: "1px solid #eee",
                  boxSizing: "border-box",
                  top: 0,
                  left: 0,
                  width: "100%",
                }}
              >
                {product.id} — {product.name} — ${product.price} —{" "}
                {product.category}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
