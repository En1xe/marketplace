import { useRef, useState, useCallback, useEffect } from "react";


export default function useWebsocket(chatUuid) {
    const [messages, setMessages] = useState([])
    const [isConnected, setIsConnected] = useState(false)
    const ws = useRef(null)

    const getWebSocketUrl = useCallback(() => {
        const host = 'localhost:8000'
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'

        return `${protocol}//${host}/chats/${chatUuid}/ws`
    }, [chatUuid])

    const sendMessage = useCallback((data) => {
        ws.current.send(JSON.stringify(data))
    }, [])

    useEffect(() => {
        const socket = new WebSocket(getWebSocketUrl())

        socket.onopen = () => {
            setIsConnected(true)
        }

        socket.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data)
                setMessages(prev => [...prev, data])
            } catch (error) {
                console.log(error)
            }
        }

        socket.onerror = (error) => {
            console.log(error)
        }

        socket.onclose = () => {
            setIsConnected(false)
        }

        ws.current = socket
        
        return () => {
            if (socket.readyState === 1) {
                ws.current.close()
                ws.current = null
            }
        };
    }, [chatUuid]);

    return {
        messages, 
        isConnected,
        sendMessage,
    }
}