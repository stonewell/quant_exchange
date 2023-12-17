import StockChart from './StockChart'

export default async function Home() {
  return (
    <main className="flex min-h-screen flex-row items-start p-5 border-b border-red-200">
      <div className="font-mono text-sm lg:flex grow">
        <StockChart />
      </div>
    </main>
  )
}
