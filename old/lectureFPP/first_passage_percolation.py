from manim import *
import numpy as np
import networkx as nx
from queue import PriorityQueue

class FirstPassagePercolation(Scene):
    def construct(self):
        # Introduction
        self.introduction()
        
        # Create a grid to demonstrate FPP
        grid_size = 5
        grid, edges, weights = self.create_weighted_grid(grid_size)
        
        # Show the grid with random weights
        self.show_weighted_grid(grid, edges, weights)
        
        # Demonstrate FPP process
        self.demonstrate_fpp(grid, edges, weights)
        
        # Show some theoretical results
        self.theoretical_results()
        
        # Conclusion
        self.conclusion()

    def introduction(self):
        title = Text("First Passage Percolation (FPP)", font_size=48)
        self.play(Write(title))
        self.wait(1)
        
        definition = Text(
            "A model that studies how fluids spread through random media",
            font_size=32
        ).next_to(title, DOWN, buff=0.5)
        
        self.play(Write(definition))
        self.wait(2)
        
        examples = VGroup(
            Text("Applications:", font_size=36),
            Text("• Flow through porous materials", font_size=28),
            Text("• Disease spread in populations", font_size=28),
            Text("• Information propagation in networks", font_size=28),
            Text("• Optimal paths in random environments", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(definition, DOWN, buff=0.7)
        
        self.play(Write(examples))
        self.wait(2)
        
        self.play(FadeOut(title), FadeOut(definition), FadeOut(examples))

    def create_weighted_grid(self, n):
        # Create a grid graph
        G = nx.grid_2d_graph(n, n)
        
        # Create positions for the nodes
        pos = {(i, j): np.array([i, j, 0]) for i in range(n) for j in range(n)}
        
        # Create random weights for edges
        edges = list(G.edges())
        weights = {e: np.random.exponential(1) for e in edges}
        
        return G, edges, weights

    def show_weighted_grid(self, G, edges, weights):
        # Title
        title = Text("Random Weighted Grid", font_size=42).to_edge(UP)
        self.play(Write(title))
        
        # Create visual grid
        n = int(np.sqrt(len(G.nodes())))
        dots = {}
        edge_lines = {}
        weight_labels = {}
        
        # Scale factor for better visualization
        scale = 1.5
        
        # Create nodes (dots)
        for i in range(n):
            for j in range(n):
                pos = np.array([i*scale-n*scale/2+scale/2, j*scale-n*scale/2+scale/2, 0])
                dot = Dot(point=pos, radius=0.1, color=BLUE)
                dots[(i, j)] = dot
                if i == 0 and j == 0:  # Source
                    dot.set_color(RED)
                
        # Create edges with weight labels
        for (i1, j1), (i2, j2) in edges:
            start_pos = dots[(i1, j1)].get_center()
            end_pos = dots[(i2, j2)].get_center()
            
            line = Line(start_pos, end_pos, stroke_width=2)
            edge_lines[((i1, j1), (i2, j2))] = line
            
            weight = weights[((i1, j1), (i2, j2))]
            weight_label = Text(f"{weight:.2f}", font_size=16, color=YELLOW)
            weight_label.move_to((start_pos + end_pos) / 2 + np.array([0, 0.2, 0]))
            weight_labels[((i1, j1), (i2, j2))] = weight_label
        
        # Add explanation
        explanation = Text(
            "In FPP, each edge has a random weight (passage time)",
            font_size=24
        ).next_to(title, DOWN)
        
        # Animation
        self.play(Write(explanation))
        
        # Draw the grid
        self.play(*[Create(dot) for dot in dots.values()])
        self.play(*[Create(line) for line in edge_lines.values()])
        self.play(*[Write(label) for label in weight_labels.values()])
        
        self.wait(2)
        
        # Highlight source and destination
        source_label = Text("Source", font_size=20, color=RED).next_to(dots[(0, 0)], DOWN, buff=0.3)
        dest_label = Text("Destination", font_size=20, color=GREEN).next_to(dots[(n-1, n-1)], UP, buff=0.3)
        
        self.play(
            dots[(n-1, n-1)].animate.set_color(GREEN),
            Write(source_label),
            Write(dest_label)
        )
        
        self.wait(1)
        
        # Store the visualization elements for later use
        self.grid_viz = {
            "dots": dots,
            "edge_lines": edge_lines,
            "weight_labels": weight_labels,
            "title": title,
            "explanation": explanation,
            "source_label": source_label,
            "dest_label": dest_label
        }

    def demonstrate_fpp(self, G, edges, weights):
        n = int(np.sqrt(len(G.nodes())))
        dots = self.grid_viz["dots"]
        edge_lines = self.grid_viz["edge_lines"]
        
        # Create a new title
        new_title = Text("FPP Process - Dijkstra's Algorithm", font_size=42).to_edge(UP)
        
        # Update explanation
        new_explanation = Text(
            "FPP finds the shortest-time path from source to destination",
            font_size=24
        ).next_to(new_title, DOWN)
        
        self.play(
            FadeOut(self.grid_viz["title"]),
            FadeOut(self.grid_viz["explanation"]),
            FadeIn(new_title),
            FadeIn(new_explanation)
        )
        
        # Run Dijkstra's algorithm to simulate FPP
        # Initialize
        source = (0, 0)
        dist = {node: float('inf') for node in G.nodes()}
        dist[source] = 0
        prev = {node: None for node in G.nodes()}
        
        pq = PriorityQueue()
        pq.put((0, source))
        
        visited = set()
        
        # Visual elements for the algorithm
        distance_labels = {}
        for node in G.nodes():
            if node == source:
                text = "0.00"
            else:
                text = "∞"
            label = Text(text, font_size=16, color=WHITE)
            label.next_to(dots[node], UP, buff=0.1)
            distance_labels[node] = label
        
        self.play(*[Write(label) for label in distance_labels.values()])
        
        # Process explanation
        process_text = Text(
            "Processing nodes in order of increasing distance...", 
            font_size=24
        ).to_edge(DOWN, buff=0.5)
        
        self.play(Write(process_text))
        
        # Run the algorithm
        visited_edges = []
        current_path = []
        
        while not pq.empty():
            current_dist, current = pq.get()
            
            if current in visited:
                continue
                
            visited.add(current)
            
            # Highlight current node
            self.play(
                dots[current].animate.set_color(YELLOW),
                distance_labels[current].animate.set_color(YELLOW)
            )
            
            self.wait(0.5)
            
            # Check if we've reached the destination
            if current == (n-1, n-1):
                break
                
            # Process neighbors
            for neighbor in G.neighbors(current):
                if neighbor in visited:
                    continue
                    
                edge = tuple(sorted([current, neighbor]))
                weight = weights[edge]
                
                # Highlight edge being considered
                self.play(
                    edge_lines[edge].animate.set_color(YELLOW).set_stroke(width=4)
                )
                
                if dist[current] + weight < dist[neighbor]:
                    old_dist = dist[neighbor]
                    dist[neighbor] = dist[current] + weight
                    prev[neighbor] = current
                    
                    # Update the distance label
                    new_label = Text(f"{dist[neighbor]:.2f}", font_size=16, color=WHITE)
                    new_label.move_to(distance_labels[neighbor])
                    
                    self.play(
                        FadeOut(distance_labels[neighbor]),
                        FadeIn(new_label)
                    )
                    
                    distance_labels[neighbor] = new_label
                    
                    # Add to priority queue
                    pq.put((dist[neighbor], neighbor))
                    
                    # If this creates a new shortest path, update
                    if old_dist == float('inf'):
                        visited_edges.append(edge)
                        self.play(
                            edge_lines[edge].animate.set_color(BLUE_B).set_stroke(width=3)
                        )
                    elif old_dist != float('inf'):
                        # Replace previous edge in path
                        old_prev = prev[neighbor]
                        if old_prev is not None:
                            old_edge = tuple(sorted([old_prev, neighbor]))
                            if old_edge in visited_edges:
                                visited_edges.remove(old_edge)
                                self.play(
                                    edge_lines[old_edge].animate.set_color(WHITE).set_stroke(width=2)
                                )
                        
                        visited_edges.append(edge)
                        self.play(
                            edge_lines[edge].animate.set_color(BLUE_B).set_stroke(width=3)
                        )
                else:
                    self.play(
                        edge_lines[edge].animate.set_color(WHITE).set_stroke(width=2)
                    )
                
                self.wait(0.5)
            
            # Reset current node color
            if current != source and current != (n-1, n-1):
                self.play(
                    dots[current].animate.set_color(BLUE),
                    distance_labels[current].animate.set_color(WHITE)
                )
        
        # Highlight the shortest path
        path = []
        current = (n-1, n-1)
        while current is not None:
            path.append(current)
            current = prev[current]
        
        path.reverse()
        
        # Create path animation
        path_edges = []
        for i in range(len(path) - 1):
            edge = tuple(sorted([path[i], path[i+1]]))
            path_edges.append(edge)
        
        # Show final path
        final_path_text = Text(
            f"Shortest path length: {dist[(n-1, n-1)]:.2f}",
            font_size=24
        ).to_edge(DOWN, buff=0.5)
        
        self.play(
            FadeOut(process_text),
            Write(final_path_text)
        )
        
        # Highlight the final path
        self.play(
            *[edge_lines[edge].animate.set_color(GREEN_B).set_stroke(width=5) 
              for edge in path_edges],
            *[dots[node].animate.set_color(GREEN if node != source else RED) 
              for node in path]
        )
        
        self.wait(2)
        
        # Clean up
        self.play(
            FadeOut(new_title),
            FadeOut(new_explanation),
            FadeOut(final_path_text),
            *[FadeOut(label) for label in distance_labels.values()]
        )

    def theoretical_results(self):
        # Title
        title = Text("Theoretical Results in FPP", font_size=42).to_edge(UP)
        self.play(Write(title))
        
        # Key results
        results = VGroup(
            Text("1. Shape Theorem", font_size=32, color=YELLOW),
            Text("As t → ∞, the set of reachable points within time t", font_size=24),
            Text("approaches a deterministic shape", font_size=24),
            
            Text("2. Time Constant", font_size=32, color=YELLOW).shift(DOWN * 1.5),
            Text("The time to reach (n,n) grows linearly with n", font_size=24),
            Text("With a constant μ (depending on the weight distribution)", font_size=24),
            
            Text("3. Fluctuations", font_size=32, color=YELLOW).shift(DOWN * 3),
            Text("Deviations from the linear growth are of order n^1/3", font_size=24),
            Text("(Conjectured but not fully proven)", font_size=24)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(title, DOWN, buff=0.5)
        
        self.play(Write(results))
        self.wait(3)
        
        self.play(FadeOut(title), FadeOut(results))

    def conclusion(self):
        # Title
        title = Text("FPP: A Model with Rich Applications", font_size=42).to_edge(UP)
        self.play(Write(title))
        
        # Conclusion points
        conclusion = VGroup(
            Text("• Mathematical model for spread through random media", font_size=28),
            Text("• Connects to shortest path problems", font_size=28),
            Text("• Has applications in:", font_size=28),
            Text("   - Epidemiology and disease spread", font_size=24),
            Text("   - Communication networks", font_size=24),
            Text("   - Fluid flow in porous media", font_size=24),
            Text("   - Growth models in biology", font_size=24),
            Text("• Active area of research in probability theory", font_size=28)
        ).arrange(DOWN, aligned_edge=LEFT).next_to(title, DOWN, buff=0.7)
        
        self.play(Write(conclusion))
        self.wait(3)
        
        final_text = Text("Thank you!", font_size=48, color=BLUE)
        self.play(FadeOut(title), FadeOut(conclusion), Write(final_text))
        self.wait(2)