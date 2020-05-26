const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';


export const getCategories = async () => {
  const response = await fetch(`${API_URL}/api/categories/`, {
    headers: {'Content-Type': 'application/json'}
  });
  return await response.json();
};

export const postOrder = async data => {
  const response = await fetch(`${API_URL}/api/make-order/`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
  });
  return await response.json();
}
