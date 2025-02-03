import axios from 'axios';
    
class ApiService {
    constructor() {
        
        

        this.instance = axios.create({
            baseURL: "http://127.0.0.1:5555",
            headers: this.getHeaders()
        });
        this.instance.interceptors.response.use(
            (response) => response,
            (error) => {
                return Promise.reject(error);
            }
        );
    }
    async sendAuthRequest(username, password) {
        const url = '/auth'; 
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        try {
            const response = await this.instance.post(url, formData, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            });
          return response;
        } catch (error) {
            console.error('Error getting access token:', error);
           throw error;
        }
    }
    

    async get(url, params = {}) {
        try {
            const response = await this.instance.get(url, { params });
            return response.data;
        } catch (error) {
            console.error('Error in GET request:', error);
            throw error;
        }
    }

    async post(url, data = {}) {
        try {
            const response = await this.instance.post(url, JSON.stringify(data));
            return response.data;
        } catch (error) {
            console.error('Error in POST request:', error);
            throw error;
        }
    }

    async put(url, data = {}) {
        try {
            const response = await this.instance.put(url, data);
            return response.data;
        } catch (error) {
            console.error('Error in PUT request:', error);
            throw error;
        }
    }

    async delete(url, params = {}) {
        try {
            const response = await this.instance.delete(url, { params });
            return response.data;
        } catch (error) {
            console.error('Error in DELETE request:', error);
            throw error;
        }
    }

    async checkUsernameAvailability(username) {
        return this.get(`/user/username`, { username });
    }

    
    getHeaders() {
        const headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        };
        
       if (process.client){
            console.log("GETTING TOKENS")
            const access_token = localStorage.getItem('access_token');
            if (access_token !== null) {
                headers.Authorization = `Bearer ${access_token}`;
            }
       }

        return headers;
    }
    
    async getMe() {
        return await this.get("/user/me")
    }
}

const apiService = new ApiService();
export default apiService;
