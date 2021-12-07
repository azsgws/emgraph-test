# test-emgraph
This graph is MML article's dependency graph.

GitHub Pages:
* Home: https://seigodev.github.io/test-emgraph/
  * article graph: https://seigodev.github.io/test-emgraph/graph/hierarchical_graph.html
  * compound graph(developping): https://seigodev.github.io/test-emgraph/compound_graph/hierarchical_graph.html

## Create graph (Create JSON file)
1. Add directory "mml" to "test-emgraph/graph".
2. Add directory "(year)-(month)-(date)"  to "test-emgraph/graph/mml".
3. Add article files to directory created by 2.
4. Move to "test-emgraph/graph"
5. Execute "python mml_graph_main.py"