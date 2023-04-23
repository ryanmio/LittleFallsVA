const axios = require('axios');
const querystring = require('querystring');
exports.handler = async (event, context) => {
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, body: 'Method Not Allowed' };
  }
console.log('event.body:', event.body);
const data = querystring.parse(event.body);



  const apiUrl = 'https://ycrm.littlefallsva.com/sites/all/modules/civicrm/extern/rest.php';
  const apiKey = 'V3llrOygSJMujjCNQ8k9Q1px';
  const siteKey = 'ywPjjLTOwbzGf2kojonJBTBROiYlFSNKWxeAh48GTfE';

try {
  console.log('Preparing to call the API...');
  
  const response = await axios.post(apiUrl, {
    entity: 'Contact',
    action: 'create',
    json: JSON.stringify({
      sequential: 1,
      contact_type: 'Individual',
      email: data.email,
      api_key: apiKey,
      key: siteKey,
    }),
  });

  console.log('API response:', response.data);

  // ... rest of the code


    if (response.data.is_error === 0) {
      return { statusCode: 200, body: 'Contact created successfully' };
    } else {
      return {
        statusCode: 500,
        body: `Error creating contact: ${response.data.error_message}`,
      };
    }
  } catch (error) {
    return { statusCode: 500, body: `Error: ${error.message}` };
  }
};
