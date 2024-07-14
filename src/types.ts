// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type Data = { [k: string]: any } | string | undefined | null

export type Command = (c: Context) => Promise<Data>
export type CommandType = 'run'

export type Context = {
  apiToken: string
  evaluationId?: string
  modelId?: string
  command: CommandType
  host: string

  commitStatusId?: string
  githubKey?: string
  repo?: string
  commit?: string
}
