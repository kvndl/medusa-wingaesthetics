const dotenv = require("dotenv");

let ENV_FILE_NAME = "";
switch (process.env.NODE_ENV) {
  case "production":
    ENV_FILE_NAME = ".env.production";
    break;
  case "staging":
    ENV_FILE_NAME = ".env.staging";
    break;
  case "test":
    ENV_FILE_NAME = ".env.test";
    break;
  case "development":
  default:
    ENV_FILE_NAME = ".env";
    break;
}

try {
  dotenv.config({ path: process.cwd() + "/" + ENV_FILE_NAME });
} catch (e) { }

// CORS when consuming Medusa from admin
const ADMIN_CORS =
  process.env.ADMIN_CORS || "http://localhost:7000,http://localhost:7001";

// CORS to avoid issues when consuming Medusa from a client
const STORE_CORS = process.env.STORE_CORS || "http://localhost:8000";

const DB_USERNAME = process.env.DB_USERNAME
const DB_PASSWORD = process.env.DB_PASSWORD
const DB_HOST = process.env.DB_HOST
const DB_PORT = process.env.DB_PORT
const DB_DATABASE = process.env.DB_DATABASE

const DATABASE_URL =
  `postgres://${DB_USERNAME}:${DB_PASSWORD}` +
  `@${DB_HOST}:${DB_PORT}/${DB_DATABASE}`

// const REDIS_URL = process.env.REDIS_URL || "redis://localhost:6379";

const plugins = [
  // {
  //   resolve: `medusa-fulfillment-webshipper`,
  //   options: {
  //     account: process.env.WEBSHIPPER_ACCOUNT,
  //     api_token: process.env.WEBSHIPPER_API_TOKEN,
  //     order_channel_id:
  //       process.env.WEBSHIPPER_ORDER_CHANNEL_ID,
  //     webhook_secret: process.env.WEBSHIPPER_WEBHOOK_SECRET,
  //     return_address: {
  //       // Webshipper Shipping Address fields
  //     },
  //     // optional
  //     coo_countries: process.env.WEBSHIPPER_COO_COUNTRIES,
  //     delete_on_cancel:
  //       process.env.WEBSHIPPER_DELETE_ON_CANCEL !== "false",
  //     document_size: process.env.WEBSHIPPER_DOCUMENT_SIZE,
  //     return_portal: {
  //       id: process.env.WEBSHIPPER_RETURN_PORTAL_ID,
  //       cause_id:
  //         process.env.WEBSHIPPER_RETURN_PORTAL_CAUSE_ID,
  //       refund_method_id:
  //         process.env.WEBSHIPPER_RETURN_REFUND_METHOD_ID,
  //     },
  //   },
  // },
  // {
  //   resolve: `medusa-plugin-mailchimp`,
  //   options: {
  //     api_key: process.env.MAILCHIMP_API_KEY,
  //     newsletter_list_id:
  //       process.env.MAILCHIMP_NEWSLETTER_LIST_ID,
  //   },
  // },
  // {
  //   resolve: `medusa-payment-stripe`,
  //   options: {
  //     api_key: process.env.STRIPE_API_KEY,
  //     webhook_secret: process.env.STRIPE_WEBHOOK_SECRET,
  //   },
  // },
  `medusa-fulfillment-manual`,
  `medusa-payment-manual`,
  {
    resolve: `@medusajs/file-local`,
    options: {
      upload_dir: "uploads",
    },
  },
  {
    resolve: `medusa-file-s3`,
    options: {
      s3_url: process.env.S3_URL,
      bucket: process.env.S3_BUCKET,
      access_key_id: process.env.S3_ACCESS_KEY_ID,
      secret_access_key: process.env.S3_SECRET_ACCESS_KEY,
    },
  },
  {
    resolve: "@medusajs/admin",
    /** @type {import('@medusajs/admin').PluginOptions} */
    options: {
      autoRebuild: true,
      develop: {
        open: process.env.OPEN_BROWSER !== "false",
      },
    },
  },
];

const modules = {
  /*eventBus: {
    resolve: "@medusajs/event-bus-redis",
    options: {
      redisUrl: REDIS_URL
    }
  },
  cacheService: {
    resolve: "@medusajs/cache-redis",
    options: {
      redisUrl: REDIS_URL
    }
  },*/


};

/** @type {import('@medusajs/medusa').ConfigModule["projectConfig"]} */
const projectConfig = {
  jwt_secret: process.env.JWT_SECRET || "supersecret",
  cookie_secret: process.env.COOKIE_SECRET || "supersecret",
  store_cors: STORE_CORS,
  database_url: DATABASE_URL,
  admin_cors: ADMIN_CORS,
  database_extra: { ssl: { rejectUnauthorized: false } }
  // redis_url: REDIS_URL
};

/** @type {import('@medusajs/medusa').ConfigModule} */
module.exports = {
  projectConfig,
  plugins,
  modules,
};
