import * as core from '@actions/core'
import {} from '@actions/github'
import type { Command, CommandType, Context, Data } from './types'
import { Post } from './server'

type Notification = {
  method: 'email' | 'webhook'
  destination: string
}
const makeCallback = ({
  commitStatusId,
  repo,
  commit,
  githubKey
}: Context): Notification[] | undefined => {
  if (!repo || !githubKey || !commit) return undefined
  const code = `
(POST(str "https://api.github.com/repos/${repo}/statuses/${commit}")
         {:headers {"X-GitHub-Api-Version" "2022-11-28"
                    "Accept" "application/vnd.github+json"
                    "Authorization"(str "Bearer ${githubKey}")}
          :json {"state"(if success "success" "failure"),
                 "target_url" report
                 "description"(if success "Evaluation session successful" "Evaluation session failed")
                "context" ${commitStatusId})`
  return [{ method: 'webhook', destination: code }]
}

const runEvalSession = async (c: Context): Promise<Data | undefined> => {
  try {
    const res = await Post(c, '/evaluationsession', {
      origin: 'user',
      evaluation_id: c.evaluationId,
      evaluatee_id: c.modelId,
      is_human_being_evaluated: false,
      notify: makeCallback({
        ...c,
        commitStatusId: c.commitStatusId || 'evaluation-session-runner'
      })
    })
    core.setOutput(
      'evaluation-session-id',
      typeof res === 'string' ? res : res?.id
    )
    return res
  } catch (e) {
    core.setFailed(`Could not start evaluation session: ${e}`)
  }
  return undefined
}

const commands = {
  run: runEvalSession
} as { [k: string]: Command }

const makeContext = (): Context => {
  const command = core.getInput('command')
  if (!['run'].includes(command)) {
    throw new Error('Invalid command provided')
  }

  return {
    command: command as CommandType,
    apiToken: core.getInput('api-token'),
    evaluationId: core.getInput('evaluation'),
    modelId: core.getInput('model'),
    host: core.getInput('host') || 'https://equistamp.net',

    githubKey: core.getInput('github-key'),
    repo: core.getInput('repository'),
    commit: core.getInput('commit'),
    commitStatusId: core.getInput('commit-status-id')
  }
}

/**
 * The main function for the action.
 * @returns {Promise<void>} Resolves when the action is complete.
 */
export async function run(): Promise<void> {
  try {
    const context = makeContext()
    const func = commands[context.command]
    if (!func) {
      core.setFailed(
        `Invalid command provided. Must be one of ${Object.keys(commands).sort()}`
      )
      return
    }
    const res = await func(context)
    core.debug(res?.toString() || 'nothing returned')

    // Set outputs for other workflow steps to use
    core.setOutput('time', new Date().toTimeString())
  } catch (error) {
    // Fail the workflow run if an error occurs
    if (error instanceof Error) core.setFailed(error.message)
  }
}
