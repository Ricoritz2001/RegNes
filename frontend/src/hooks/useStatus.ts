import { useState, useEffect} from 'react'
import { getStatus, StatusResponse} from '../services/api'

export function useStatus() {
    const [data, setData] = useState<StatusResponse | null>(null)
    const [loading, setLoading] = useState<boolean>(true)
    const [error, setError] = useState<string | null>(null)
  
    useEffect(() => {
      getStatus()
        .then((resp) => {
          setData(resp)
        })
        .catch((err) => {
          console.error(err)
          setError(err.message || 'Failed to fetch status')
        })
        .finally(() => {
          setLoading(false)
        })
    }, [])
  
    return { data, loading, error }
  }

