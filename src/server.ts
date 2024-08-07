import { Context, Data } from './types'

export class ServerError extends Error {
  status: number
  error: Data

  constructor(status: number, error: Data) {
    super()
    this.status = status
    this.error = error
  }
}

const paramsString = (params?: Data): string => {
  if (!params) return ''
  const vals = Object.entries(params)
    .filter(([k, v]) => k && v !== undefined && v !== null)
    .map(([k, v]) => `${k}=${v}`)
    .join('&')
  return `?${vals}`
}

const retryFetch = async (
  url: string,
  options: RequestInit = {},
  maxRetries = 3
): Promise<Response> => {
  for (let retries = 0; retries < maxRetries; retries++) {
    try {
      const response = await fetch(url, options)
      if (response.status !== 504) return response
    } catch (error) {
      const delay = Math.pow(2, retries) * 1000
      await new Promise(resolve => setTimeout(resolve, delay))
    }
  }
  throw new Error('Max retries reached')
}

export const query = async (
  { host, apiToken }: Context,
  callEndpoint: string,
  data?: Data,
  callMethod?: string
): Promise<Data> => {
  const method = callMethod || 'GET'
  const endpoint = ['GET', 'DELETE'].includes(method)
    ? callEndpoint + paramsString(data)
    : callEndpoint
  const body = ['POST', 'PUT'].includes(method)
    ? data && JSON.stringify(data)
    : undefined

  const getContents = async (resp: Response): Promise<Data> => {
    const contentType = resp.headers.get('Content-Type') || 'application/json'
    if (contentType === 'application/json') {
      return resp.json()
    } else if (contentType === 'text/csv') {
      return resp.blob()
    }
    return resp.text()
  }

  const resp = await retryFetch(`${host}${endpoint}`, {
    method,
    body,
    headers: {
      'Content-Type': 'application/json',
      'api-token': apiToken
    }
  })
  if (!resp.ok) {
    throw new ServerError(resp.status, await getContents(resp))
  }
  return getContents(resp)
}

export const Get = async (
  context: Context,
  endpoint: string,
  params?: Data
): Promise<Data> => query(context, endpoint, params)
export const Post = async (
  context: Context,
  endpoint: string,
  data: Data
): Promise<Data> => query(context, endpoint, data, 'POST')
export const Put = async (
  context: Context,
  endpoint: string,
  data: Data
): Promise<Data> => query(context, endpoint, data, 'PUT')
export const Delete = async (
  context: Context,
  endpoint: string,
  params?: Data
): Promise<Data> => query(context, endpoint, params, 'DELETE')
