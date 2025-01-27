<template>
  <div class="market-dashboard">
    <h2>Market Data</h2>
    <div class="market-grid">
      <div
        v-for="asset in assets"
        :key="asset.symbol"
        class="asset-card"
        :class="{
          'price-up': asset.change > 0,
          'price-down': asset.change < 0,
        }"
      >
        <div class="asset-header">
          <span class="asset-symbol">{{ asset.symbol }}</span>
          <span class="asset-price">${{ formatPrice(asset.price) }}</span>
          <span
            class="asset-change"
            :class="{ positive: asset.change > 0, negative: asset.change < 0 }"
          >
            {{ asset.change > 0 ? "+" : "" }}{{ asset.change.toFixed(1) }}%
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";

const assets = ref([
  { symbol: "BTC", name: "Bitcoin", price: 0, change: 0 },
  { symbol: "ETH", name: "Ethereum", price: 0, change: 0 },
  { symbol: "GOLD", name: "Gold", price: 0, change: 0 },
  { symbol: "SILVER", name: "Silver", price: 0, change: 0 },
  { symbol: "EUR", name: "Euro", price: 0, change: 0 },
  { symbol: "GBP", name: "British Pound", price: 0, change: 0 },
]);

const API_KEY = "YOUR_API_KEY"; // You'll need to sign up for a free API key
const updateInterval = ref(null);

const formatPrice = (price) => {
  return price.toLocaleString("en-US", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
};

const fetchMarketData = async () => {
  try {
    // Example using CoinGecko API for crypto (free, no API key needed)
    const cryptoResponse = await fetch(
      "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true"
    );
    const cryptoData = await cryptoResponse.json();

    // Update crypto prices
    assets.value.forEach((asset) => {
      if (asset.symbol === "BTC") {
        asset.price = cryptoData.bitcoin.usd;
        asset.change = cryptoData.bitcoin.usd_24h_change;
      } else if (asset.symbol === "ETH") {
        asset.price = cryptoData.ethereum.usd;
        asset.change = cryptoData.ethereum.usd_24h_change;
      }
    });

    // Simulate other asset prices for demo (replace with real API data)
    assets.value.forEach((asset) => {
      if (!["BTC", "ETH"].includes(asset.symbol)) {
        const randomChange = (Math.random() * 2 - 1).toFixed(2);
        asset.change = parseFloat(randomChange);
        if (asset.symbol === "GOLD")
          asset.price = 1900 + (Math.random() * 20 - 10);
        if (asset.symbol === "SILVER")
          asset.price = 23 + (Math.random() * 2 - 1);
        if (asset.symbol === "EUR")
          asset.price = 1.08 + (Math.random() * 0.02 - 0.01);
        if (asset.symbol === "GBP")
          asset.price = 1.26 + (Math.random() * 0.02 - 0.01);
      }
    });
  } catch (error) {
    console.error("Error fetching market data:", error);
  }
};

onMounted(() => {
  fetchMarketData();
  updateInterval.value = setInterval(fetchMarketData, 30000); // Update every 30 seconds
});

onUnmounted(() => {
  if (updateInterval.value) clearInterval(updateInterval.value);
});
</script>

<style scoped>
.market-dashboard {
  position: fixed;
  left: 40px;
  top: 80px;
  transform: none;
  width: 280px;
  background: rgba(26, 35, 126, 0.4);
  backdrop-filter: blur(10px);
  border: 1px solid var(--bank-gold);
  border-radius: 12px;
  padding: 1rem;
}

.market-dashboard h2 {
  color: var(--bank-gold);
  text-align: center;
  margin-bottom: 1rem;
  font-size: 1.2rem;
  font-weight: 600;
}

.market-grid {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.asset-card {
  padding: 0.5rem;
  border-bottom: 1px solid rgba(207, 181, 59, 0.2);
  transition: all 0.3s ease;
}

.asset-card:last-child {
  border-bottom: none;
}

.asset-card:hover {
  background: rgba(26, 35, 126, 0.6);
}

.asset-header {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 1rem;
}

.asset-symbol {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--bank-gold);
}

.asset-price {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--bank-white);
  text-align: right;
}

.asset-change {
  font-size: 0.8rem;
  font-weight: 500;
  min-width: 60px;
  text-align: right;
}

.asset-change.positive {
  color: #4caf50;
}

.asset-change.negative {
  color: #f44336;
}

.price-up {
  animation: priceUp 0.5s ease-out;
}

.price-down {
  animation: priceDown 0.5s ease-out;
}

@keyframes priceUp {
  0% {
    background-color: rgba(76, 175, 80, 0.1);
  }
  100% {
    background-color: transparent;
  }
}

@keyframes priceDown {
  0% {
    background-color: rgba(244, 67, 54, 0.1);
  }
  100% {
    background-color: transparent;
  }
}

@media (max-width: 1024px) {
  .market-dashboard {
    position: static;
    transform: none;
    width: 100%;
    max-width: 280px;
    margin: 1rem auto;
  }
}
</style>
