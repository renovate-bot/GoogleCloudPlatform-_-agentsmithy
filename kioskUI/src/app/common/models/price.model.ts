export const SETUP_PRICES: ServicePrice[] = [
    {
        service: "VertexAI",
        prices: [
            {
                type: "PAID",
                price: 0.000759,
                description: "Default Intents Data Size: 0.000254 GiB * $3/GiB",
            } 
        ]
    },
    {
        service: "Generative AI",
        prices: [
            {
                type: "PAID",
                price: 0.0002758,
                description: "Default Intents Embeddings: 11032 characters * $0.000025 / 1,000 characters",
            } 
        ]
    },
]

export const OPERATIONS_PRICES: ServicePrice[] = [
    {
        service: "Cloud Run",
        prices: [
            {
                type: "FREE",
                price: 0,
                description: "First 180,000 vCPU-seconds free per month"
            },
            {
                type: "FREE",
                price: 0,
                description: "First 360,000 GiB-seconds free per month"
            },
            {
                type: "FREE",
                price: 0,
                description: "2 million requests free per month"
            },
            {
                type: "PAID",
                price: 0.00002400,
                description: "$0.00002400 / vCPU-second"
            },
            {
                type: "PAID",
                price: 0.00000250,
                description: "$0.00000250 / GiB-second"
            },
        ]
    },
    {
        service: "Artifact Registry",
        prices: [
            {
                type: "FREE",
                price: 0,
                description: "Up to 0.5 GB Free"
            },
            {
                type: "PAID",
                price: 0.10,
                description: "$0.10 per GB / month"
            },
        ]
    },
    {
        service: "Cloud Build",
        prices: [
            {
                type: "FREE",
                price: 0,
                description: "First 2,500 builds-minutes"
            },
            {
                type: "PAID",
                price: 0.006,
                description: "$0.006 / build-minute"
            },
        ]
    },
    {
        service: "Cloud Storage",
        prices: [
            {
                type: "FREE",
                price: 0,
                description: "Standard storage: 5 GB-months"
            },
            {
                type: "FREE",
                price: 0,
                description: "Class A Operations: 5,000"
            },
            {
                type: "FREE",
                price: 0,
                description: "Class B Operations: 50,000"
            },
            {
                type: "PAID",
                price: 0.020,
                description: "$0.020 per GB per Month"
            },
            {
                type: "PAID",
                price: 0.0050,
                description: "$0.0050 per 1,000 class A operations"
            },
            {
                type: "PAID",
                price: 0.0004,
                description: "$0.0004, per 1,000 class B operations"
            },
        ]
    },
    {
        service: "BigQuery",
        prices: [
            {
                type: "FREE",
                price: 0,
                description: "Querying: 1TiB"
            },
            {
                type: "FREE",
                price: 0,
                description: "Storage: 10GiB"
            },
            {
                type: "PAID",
                price: 6.25,
                description: "Querying: $6.25 per TiB"
            },
            {
                type: "PAID",
                price: 0.02,
                description: "Storage: $0.02 per GiB"
            },
        ]
    },
    {
        service: "VertexAI",
        prices: [
            {
                type: "PAID",
                price: 3,
                description: "Building cost: data size(in GiB) * $3/GiB * # of updates/month"
            },
            {
                type: "PAID",
                price: 0.094,
                description: "Serving cost: # replicas/shard * # shards (~data size/shard size) * $0.094/hour"
            },
        ]
    },
    {
        service: "Generative AI",
        prices: [
            {
                type: "PAID",
                price: 0.000025,
                description: "Generating embeddings for question: $0.000025 per 1,000 characters"
            },
            {
                type: "PAID",
                price: 0.00001875,
                description: "Input tokens: $0.00001875 / 1k characters"
            },
            {
                type: "PAID",
                price: 0.000075,
                description: "Output tokens: $0.000075 / 1k characters"
            },
        ]
    },
]

export type Price = {
    type: "FREE" | "PAID"
    description: string
    price: number
}

export type ServicePrice = {
    service: string
    prices: Price[]
}