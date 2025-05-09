let socket = null;
let subscribers = new Set();

export function connectWS(url) {
    if (!socket || socket.readyState !== WebSocket.OPEN) {
        socket = new WebSocket(url)

        socket.onopen = () => {
            console.log("Websocket connected")
        }

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data)
            subscribers.forEach((handler) => handler(data))
        }

        socket.onclose = () => {
            console.log("Websocket closed")
            socket = null
        }

        socket.onerror = (error) => {
            console.error("Websocket error", error)
        }
    }
}

export function subscribeWS(handler) {
    subscribers.add(handler)
}

export function unsubscribeWS(handler) {
    subscribers.delete(handler)
    if (subscribers.size === 0 && socket) {
        socket.close()
    }
}



