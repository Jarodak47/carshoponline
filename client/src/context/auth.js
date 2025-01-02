import axios from "axios";
import { createContext, useContext, useEffect, useState } from "react";


const AuthContext = createContext()

const AuthProvider = ({children}) => {
    const [auth,setAuth] = useState({
        user:null,
        token:''
    })
        
    // Mettre à jour les en-têtes par défaut d'axios avec le token
    useEffect(() => {
        if (auth?.token?.access_token) {
            axios.defaults.headers.common['Authorization'] = `Bearer ${auth?.token?.access_token}`;
        } else {
            delete axios.defaults.headers.common['Authorization'];
        }
    }, [auth?.token]);


    useEffect(() => {
        const data = localStorage.getItem('auth')
        if(data){
            const parseData = JSON.parse(data)
            setAuth({
                ...auth,
                user:parseData.user,
                token:parseData.token
            })
        }
    },[])
    return (
        <AuthContext.Provider value={[auth,setAuth]}>
            {children}
        </AuthContext.Provider>
    )
}

const useAuth = () => useContext(AuthContext)

export {useAuth,AuthProvider}