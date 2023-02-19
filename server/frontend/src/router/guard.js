import ApolloClient from 'apollo-boost'
import gql from 'graphql-tag'

const apolloClient = new ApolloClient({
  // You should use an absolute URL here
  uri: '/api/'
})

export function graud(to, from, next) {
  apolloClient.query({
    query: gql`
      query {
        identity { 
          id
          isSuperuser
          username
        }
      }
    `
  }).then( (data) => {
    if (data.identity !== null) {
      next();
    } else {
      next({ name: "Login" });
    }
  }).catch( (error) => {
    next({ name: "Login" });
  })
}