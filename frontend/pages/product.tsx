import { useRouter } from 'next/router';
import useSWR from 'swr';
import { fetcher } from '../lib/fetcher';

type Product = {
  id: number;
  name: string;
  description: string;
  price: number;
  category: string;
};

export default function ProductPage() {
  const router = useRouter();
  const { id } = router.query;

  const { data, error } = useSWR<Product>(
    id ? `http://localhost:8000/products/${id}` : null,
    fetcher
  );

  if (error) return <div>Error loading product</div>;
  if (!data) return <div>Loading...</div>;

  return (
    <div style={{ padding: 20 }}>
      <h1>{data.name}</h1>
      <p>{data.description}</p>
      <p><strong>Price:</strong> ${data.price}</p>
      <p><strong>Category:</strong> {data.category}</p>
      <button onClick={() => router.back()}>Go back</button>
    </div>
  );
}