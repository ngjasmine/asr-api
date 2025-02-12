import React from "react";

import ElasticsearchAPIConnector from "@elastic/search-ui-elasticsearch-connector";


import {
  ErrorBoundary,
  Facet,
  SearchProvider,
  SearchBox,
  Results,
  PagingInfo,
  ResultsPerPage,
  Paging,
  Sorting,
  WithSearch
} from "@elastic/react-search-ui";
import { Layout } from "@elastic/react-search-ui-views";
import "@elastic/react-search-ui-views/lib/styles/styles.css";

// import {
//   buildAutocompleteQueryConfig,
//   buildFacetConfigFromConfig,
//   buildSearchOptionsFromConfig,
//   buildSortOptionsFromConfig,
//   getConfig,
//   getFacetFields
// } from "./config/config-helper";

// const { hostIdentifier, searchKey, endpointBase, engineName } = getConfig();
const connector = new ElasticsearchAPIConnector({
  host: process.env.REACT_APP_ELASTIC_ENDPOINT,  // Use 'endpoint' instead of 'cloud'
  apiKey: process.env.REACT_APP_ELASTIC_API_KEY,
  index: process.env.REACT_APP_INDEX_NAME
});
const config = {
  searchQuery: {
    search_fields: {
      // We're prioritizing the full-text field "generated_text"
      generated_text: { weight: 3 }
    },
    result_fields: {
      // Return a snippet for the generated_text field
      generated_text: {
        snippet: {
          size: 100,
          fallback: true
        }
      },
      // Also display these fields as raw values
      duration: { raw: {} },
      age: { raw: {} },
      gender: { raw: {} },
      accent: { raw: {} }
    },
    // Facets that users can filter by (for exact matching)
    disjunctiveFacets: ["age", "gender", "accent"],
    facets: {
      age: { type: "value" },
      gender: { type: "value" },
      accent: { type: "value" },
      // If you want to filter by duration ranges, define a range facet.
      duration: {
        type: "range",
        ranges: [
          { to: 1, name: "Under 1 sec" },
          { from: 1, to: 3, name: "1 to 3 sec" },
          { from: 3, name: "3+ sec" }
        ]
      }
    }
  },
  autocompleteQuery: {
    results: {
      resultsPerPage: 5,
      search_fields: {
        // Use the "suggest" sub-field for autocomplete
        "generated_text.suggest": { weight: 3 }
      },
      result_fields: {
        generated_text: {
          snippet: {
            size: 100,
            fallback: true
          }
        }
      }
    },
    suggestions: {
      types: {
        results: { fields: ["generated_text.suggest"] }
      },
      size: 4
    }
  },
  apiConnector: connector,
  alwaysSearchOnInitialLoad: true
};

export default function App() {
  return (
    <SearchProvider config={config}>
      <WithSearch mapContextToProps={({ wasSearched }) => ({ wasSearched })}>
        {({ wasSearched }) => (
          <div className="App">
            <ErrorBoundary>
              <Layout
                // Update the SearchBox for autocomplete as described in the tutorial.
                header={
                  <SearchBox
                    autocompleteMinimumCharacters={3}
                    autocompleteResults={{
                      linkTarget: "_blank",
                      sectionTitle: "Results",
                      titleField: "generated_text", // Use your field here
                      shouldTrackClickThrough: true
                    }}
                    autocompleteSuggestions={true}
                    debounceLength={0}
                  />
                }
                // Side content: remove sorting options (empty sortOptions) and add facets.
                sideContent={
                  <div>
                    {wasSearched && <Sorting label={"Sort by"} sortOptions={[]} />}
                    <Facet key={"1"} field={"age"} label={"Age"} />
                    <Facet key={"2"} field={"gender"} label={"Gender"} />
                    <Facet key={"3"} field={"accent"} label={"Accent"} />
                    <Facet key={"4"} field={"duration"} label={"Duration"} />
                  </div>
                }
                // Update Results to display your generated_text field.
                bodyContent={
                  <Results
                    titleField="generated_text"
                    shouldTrackClickThrough={true}
                  />
                }
                bodyHeader={
                  <>
                    {wasSearched && <PagingInfo />}
                    {wasSearched && <ResultsPerPage />}
                  </>
                }
                bodyFooter={<Paging />}
              />
            </ErrorBoundary>
          </div>
        )}
      </WithSearch>
    </SearchProvider>
  );
}
//   return (
//     <SearchProvider config={config}>
//       <WithSearch mapContextToProps={({ wasSearched }) => ({ wasSearched })}>
//         {({ wasSearched }) => {
//           return (
//             <div className="App">
//               <ErrorBoundary>
//                 <Layout
//                   header={<SearchBox autocompleteSuggestions={true} />}
//                   sideContent={
//                     <div>
//                       {wasSearched && (
//                         <Sorting
//                           label={"Sort by"}
//                           sortOptions={buildSortOptionsFromConfig()}
//                         />
//                       )}
//                       {getFacetFields().map(field => (
//                         <Facet key={field} field={field} label={field} />
//                       ))}
//                     </div>
//                   }
//                   bodyContent={
//                     <Results
//                       titleField={getConfig().titleField}
//                       urlField={getConfig().urlField}
//                       thumbnailField={getConfig().thumbnailField}
//                       shouldTrackClickThrough={true}
//                     />
//                   }
//                   bodyHeader={
//                     <React.Fragment>
//                       {wasSearched && <PagingInfo />}
//                       {wasSearched && <ResultsPerPage />}
//                     </React.Fragment>
//                   }
//                   bodyFooter={<Paging />}
//                 />
//               </ErrorBoundary>
//             </div>
//           );
//         }}
//       </WithSearch>
//     </SearchProvider>
//   );
// }
