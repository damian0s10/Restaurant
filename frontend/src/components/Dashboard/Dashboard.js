import React, {useEffect, useState} from "react";
import {getCategories, postOrder} from "../../services/api";
import './styles.scss';


const Dashboard = () => {
  const [categories, setCategories] = useState([]);
  const [basket, setBasket] = useState({});
  const [result, setResult] = useState([]);

  useEffect(() => {
    getCategories()
      .then(res => {
        setCategories(res);
      })
      .catch(err => {
        console.log(err.response);
      });
  }, []);

  const addToBasket = product => {
    let count = basket?.[product.id]?.count || 0;
    setBasket({...basket, [product.id]: {product, count: count + 1}})
  };

  const renderProduct = product => {
    return (
      <li key={product.id}>
        <h2>
          {product.name}
        </h2>
        <div className='product product__container'>
          <div className='product__description'>
            {product.description}
          </div>
          <div className='product__price'>
            {product.price} zł
          </div>
          <div className='product__action'>
            <button type='button' onClick={() => addToBasket(product)}>+</button>
          </div>
        </div>
      </li>
    )
  };

  const renderCategory = category => {
    if (category) {
      return (
        <section key={category.id}>
          <header>
            <h1>
              {category.name}
            </h1>
          </header>
          <hr/>
          <ul>
            {category?.products?.map(product => ({...product, category: category.name})).map(renderProduct)}
          </ul>
        </section>
      )
    }
    return false
  };

  const renderCategories = () => {
    if (categories?.length) {
      return categories.map(renderCategory);
    }
    return false;
  };

  const orderFood = () => {
    const products = Object.values(basket).map(item => ({...item.product, count: item.count}))
    postOrder(products)
      .then(response => setResult(response.data))
      .catch(error => console.error(error));
  };

  const renderContent = () => {
    if (result.length) {
      return (
        <ul style={{margin: 40}}>
          {result.map((item, index) => <li key={index} style={{marginBottom: 10}}>
            {!!item.total_price &&
            [<span style={{fontWeight: 'bold'}}>Cena całkowita </span>, item.total_price]}
            {!!item.price &&
            [<span style={{fontWeight: 'bold'}}>{item.name} </span>, item.price]} zł
          </li>)}
        </ul>
      );
    }

    return (
      <>
        <main style={{marginRight: '15px'}}>
          {renderCategories()}
        </main>
        <aside style={{marginLeft: '15px', marginRight: '15px', maxWidth: 300, width: '100%'}}>
          <h1 style={{margin: 10, textAlign: 'center'}}>Koszyk</h1>
          <ul>
            {Object.keys(basket).length === 0 && <li key='empty-basket' style={{marginBottom: 10}}>Koszyk jest pusty</li>}
            {Object.values(basket).map(item => <li key={item.product.id} style={{marginBottom: 10}}>
              {item.product.name} x{item.count}
            </li>)}
          </ul>
          {!!Object.keys(basket).length && <button type='button' onClick={orderFood}>Zamów</button>}
        </aside>
      </>
    )
  }


  return (
    <div className='dashboard dashboard__container'>
      {renderContent()}
    </div>
  );
};

export default Dashboard;
