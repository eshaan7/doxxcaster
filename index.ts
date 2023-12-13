import 'dotenv/config'
import yargs from 'yargs'
import { hideBin } from 'yargs/helpers'
import { Client } from '@xmtp/xmtp-js'
import { Wallet } from 'ethers'

yargs(hideBin(process.argv))
    .command(
        'send <address> <message>',
        'Send a message to a blockchain address',
        {
            address: { type: 'string', demand: true },
            message: { type: 'string', demand: true },
        },
        async (argv: any) => {
            const { env, message, address } = argv
            const wallet = Wallet.fromMnemonic(process.env.FARCASTER_MNEMONIC as string)
            const client = await Client.create(wallet, { env })
            const isOnXmtp = await client.canMessage(address)
            if (isOnXmtp) {
                const conversation = await client.conversations.newConversation(address)
                const sent = await conversation.send(message)
                if (sent.error == undefined) console.log(sent.id)
            } else {
                console.log(null)
            }
        }
    )
    .option('env', {
        alias: 'e',
        type: 'string',
        default: 'dev',
        choices: ['dev', 'production', 'local'] as const,
        description: 'The XMTP environment to use',
    })
    .demandCommand(1)
    .parse()