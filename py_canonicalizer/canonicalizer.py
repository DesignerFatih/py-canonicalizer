import numpy as np

# --- Component Inputs ---
# points_in: A NumPy array representing 3D coordinates.
# remove_duplicates: True to remove duplicate points (for closed polylines).
# --- Component Output ---
# points_out: The final canonical NumPy array.
points_out = None

if points_in is not None:
    print("--- DEBUG: Canonicalization Started ---")
    
    # --- 1. Data Cleaning Rule ---
    # Check if the polyline is closed by comparing the first and last points.
    # If it's closed and the user wants to remove duplicates, remove the last point.
    if remove_duplicates and np.allclose(points_in[0], points_in[-1]):
        M = points_in[:-1]
        print("DEBUG: Duplicate point removal is active. Last point removed.")
    else:
        M = points_in
    
    N = M.shape[0]
    print(f"DEBUG: Total number of unique points to process (N): {N}")
    
    # Handle polylines with less than 3 points
    if N < 3:
        points_out = M
    else:
        # --- 2. Find Centroid and Distances ---
        C = np.mean(M, axis=0)
        distances = np.linalg.norm(M - C, axis=1)
        min_dist = np.min(distances)
        min_dist_indices = np.where(np.isclose(distances, min_dist))[0]
        
        # --- 3. Determine Start Index (Hierarchical Tie-breaker) ---
        if len(min_dist_indices) == 1:
            start_idx = min_dist_indices[0]
        else:
            tied_points = M[min_dist_indices]
            sort_indices = np.lexsort((tied_points[:, 2], tied_points[:, 1], tied_points[:, 0]))
            winner_idx_in_tied = sort_indices[-1]
            start_idx = min_dist_indices[winner_idx_in_tied]

        print(f"DEBUG: Start Index (I_start): {start_idx}")

        # --- 4. Determine Direction ---
        I_prev = (start_idx - 1 + N) % N
        I_next = (start_idx + 1) % N
        P_prev = M[I_prev]
        P_next = M[I_next]
        
        is_forward = True
        if P_prev[0] > P_next[0]: is_forward = False
        elif P_prev[0] == P_next[0] and P_prev[1] > P_next[1]: is_forward = False
        elif P_prev[0] == P_next[0] and P_prev[1] == P_next[1] and P_prev[2] > P_next[2]: is_forward = False
        
        # --- 5. Create the Final Canonical List ---
        shifted_indices = np.roll(np.arange(N), -start_idx)
        M_canonical = M[shifted_indices]
        
        if not is_forward:
            M_canonical = np.concatenate((M_canonical[0:1], M_canonical[1:][::-1]))
            
        # Assign the result to the output variable
        points_out = M_canonical
    
    print("--- DEBUG: Canonicalization Finished ---")