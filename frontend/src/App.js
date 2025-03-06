import React, { useState } from 'react';
import './App.css';


const DEFAULT_IMAGE = './src/images/img.png';

function App() {
  const [gameName, setGameName] = useState('');
  const [stores, setStores] = useState({
    platimarket: false,
    steambuy: false,
    steam_account: false
  });
  const [sorting, setSorting] = useState({ min: false, max: false });
  const [priceRange, setPriceRange] = useState({ min: '', max: '' });
  const [games, setGames] = useState([]);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [showAbout, setShowAbout] = useState(false);

  const handleSearch = async () => {
    setError(null);
    setIsLoading(true);
    let results = [];
    const baseUrl = "http://192.168.0.120:8000";
    console.log("BackendURL: ", baseUrl);

    const fetchData = async (url, storeName) => {
      try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`${storeName} Error: ${response.statusText}`);
        const data = await response.json();
        return Array.isArray(data) ? data : [data];
      } catch (error) {
        console.error(`Error fetching data from ${storeName}:`, error);
        return [];
      }
    };

    try {
      if (stores.platimarket) {
        if (sorting.min) {
          const data = await fetchData(`${baseUrl}/min_plati/${encodeURIComponent(gameName)}`, 'PlatiMarket');
          results = results.concat(data);
        }
        if (sorting.max) {
          const data = await fetchData(`${baseUrl}/max_plati/${encodeURIComponent(gameName)}`, 'PlatiMarket');
          results = results.concat(data);
        }
        if (priceRange.min && priceRange.max) {
          const data = await fetchData(`${baseUrl}/get_range_plati/${encodeURIComponent(gameName)}&min=${priceRange.min}&max=${priceRange.max}?direction=true`, 'PlatiMarket');
          results = results.concat(data);
        }
      }

      if (stores.steambuy) {
        if (sorting.min) {
          const data = await fetchData(`${baseUrl}/get_min_steambuy/${encodeURIComponent(gameName)}`, 'SteamBuy');
          results = results.concat(data);
        }
        if (sorting.max) {
          const data = await fetchData(`${baseUrl}/get_max_steambuy/${encodeURIComponent(gameName)}`, 'SteamBuy');
          results = results.concat(data);
        }
        if (priceRange.min && priceRange.max) {
          const data = await fetchData(`${baseUrl}/get_range_steambuy/${encodeURIComponent(gameName)}&min=${priceRange.min}&max=${priceRange.max}?direction=true`, 'SteamBuy');
          results = results.concat(data);
        }
      }

      if (stores.steam_account) {
        if (sorting.min) {
          const data = await fetchData(`${baseUrl}/get_min_steam_account/${encodeURIComponent(gameName)}`, 'Steam Account');
          results = results.concat(data);
        }
        if (sorting.max) {
          const data = await fetchData(`${baseUrl}/get_max_steam_account/${encodeURIComponent(gameName)}`, 'Steam Account');
          results = results.concat(data);
        }
        if (priceRange.min && priceRange.max) {
          const data = await fetchData(`${baseUrl}/get_range_steam_accounts/${encodeURIComponent(gameName)}&min=${priceRange.min}&max=${priceRange.max}?direction=true`, 'Steam Account');
          results = results.concat(data);
        }
      }

      if (sorting.min) {
        results.sort((a, b) => a.price - b.price);
      } else if (sorting.max) {
        results.sort((a, b) => b.price - a.price);
      }

      setGames(results);
    } catch (error) {
      setError(error.message);
      console.error("Error fetching data:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app">
      <div className="about-link" onClick={() => setShowAbout(true)}>
        About
      </div>

      {/* Модальное окно About */}
      {showAbout && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h2>О нашем сервисе</h2>
            <p>
            Добро пожаловать в Keys Bank! Наш сервис позволяет сравнивать цены на игры на разных платформах, включая PlatiMarket, SteamBuy и Steam Account. Вы можете искать игры, фильтровать по ценовому диапазону и сортировать по минимальной или максимальной цене.
            </p>
            <p>
            Наша цель — помочь вам найти лучшие предложения на ваши любимые игры. Ищете ли вы самый дешевый вариант или самое премиальное издание, мы вам поможем.
            </p>
            <p>
              Если у вас есть предложения, или вы желаете сотрудничать, не стесняйтесь писать на коммерческую почту: supkeysbank@gmail.com
            </p>
            <p>
              Спасибо, что выбираете нас!
            </p>
            <button className="close-button" onClick={() => setShowAbout(false)}>
              Закрыть
            </button>
          </div>
        </div>
      )}

      <h1>Keys Bank</h1>
      <SearchBar gameName={gameName} setGameName={setGameName} stores={stores} setStores={setStores} />
      <SortingOptions sorting={sorting} setSorting={setSorting} priceRange={priceRange} setPriceRange={setPriceRange} />
      <button className="search-button" onClick={handleSearch} disabled={isLoading}>
        {isLoading ? 'Searching...' : 'Поиск'}
      </button>
      {error && <p className="error-message">{error}</p>}
      {isLoading ? (
        <div className="loading-animation">
          <div className="spinner"></div>
        </div>
      ) : (
        <GameList games={games} />
      )}

      <div className="disclaimer">
        Мы не несем ответственность за точность цен, наличие товаров и другие аспекты, связанные с магазинами. Все данные предоставляются исключительно в ознакомительных целях.
      </div>
    </div>
  );
}

function SearchBar({ gameName, setGameName, stores, setStores }) {
  const [showStoreDropdown, setShowStoreDropdown] = useState(false);

  const handleStoreChange = (store) => {
    setStores({ ...stores, [store]: !stores[store] });
  };

  return (
    <div className="search-bar">
      <input
        type="text"
        value={gameName}
        onChange={(e) => setGameName(e.target.value)}
        placeholder="Введите название игры"
        className="game-input"
      />
      <div className="store-dropdown">
        <button className="store-dropdown-button" onClick={() => setShowStoreDropdown(!showStoreDropdown)}>
          Магазины
        </button>
        {showStoreDropdown && (
          <div className="store-dropdown-content">
            <label>
              <input
                type="checkbox"
                checked={stores.platimarket}
                onChange={() => handleStoreChange('platimarket')}
              />
              PlatiMarket
            </label>
            <label>
              <input
                type="checkbox"
                checked={stores.steambuy}
                onChange={() => handleStoreChange('steambuy')}
              />
              SteamBuy
            </label>
            <label>
              <input
                type="checkbox"
                checked={stores.steam_account}
                onChange={() => handleStoreChange('steam_account')}
              />
              Steam Account
            </label>
          </div>
        )}
      </div>
    </div>
  );
}

function SortingOptions({ sorting, setSorting, priceRange, setPriceRange }) {
  const handleSortingChange = (type) => {
    setSorting({ ...sorting, [type]: !sorting[type] });
  };

  return (
    <div className="sorting-options">
      <label>
        <input type="checkbox" checked={sorting.min} onChange={() => handleSortingChange('min')} />
        Дешевые
      </label>
      <label>
        <input type="checkbox" checked={sorting.max} onChange={() => handleSortingChange('max')} />
        Дорогие
      </label>
      <div className="price-range">
        <input
          type="number"
          value={priceRange.min}
          onChange={(e) => setPriceRange({ ...priceRange, min: e.target.value })}
          placeholder="Цена от"
        />
        <input
          type="number"
          value={priceRange.max}
          onChange={(e) => setPriceRange({ ...priceRange, max: e.target.value })}
          placeholder="до"
        />
      </div>
    </div>
  );
}

function GameList({ games }) {
  return (
    <div className="game-list">
      {games.map((game, index) => (
        <div key={index} className="game-card">
          <img
            src={
              game.image
                ? game.image.startsWith('//')
                  ? `https:${game.image}`
                  : game.image
                : DEFAULT_IMAGE
            }
            alt={game.name}
            className="game-image"
          />
          <h3>{game.name}</h3>
          <p>Price: {game.price} ₽</p>
          <a href={game.url} target="_blank" rel="noopener noreferrer" className="buy-button">
            Купить
          </a>
        </div>
      ))}
    </div>
  );
}

export default App;
