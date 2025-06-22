import logging
import numpy as np
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session

from app.models.analysis import (
    Analysis, AnalysisType, NodeResult, ElementResult, ModalResult
)
from app.models.node import Node
from app.models.element import Element
from app.models.load import Load, LoadCase, LoadCombination, LoadCombinationCase
from app.models.material import Material
from app.models.section import Section

logger = logging.getLogger(__name__)


class StructuralAnalysisSolver:
    """
    Structural analysis solver for various analysis types.
    """
    
    def __init__(self, db: Session, analysis_id: str):
        """
        Initialize the solver with database session and analysis ID.
        """
        self.db = db
        self.analysis_id = analysis_id
        self.analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        
        if not self.analysis:
            raise ValueError(f"Analysis with ID {analysis_id} not found")
        
        self.project_id = self.analysis.project_id
        
        # Load model data
        self.nodes = db.query(Node).filter(Node.project_id == self.project_id).all()
        self.elements = db.query(Element).filter(Element.project_id == self.project_id).all()
        
        # Load cases and combinations
        self.load_cases = []
        if self.analysis.load_case_ids:
            self.load_cases = db.query(LoadCase).filter(
                LoadCase.id.in_(self.analysis.load_case_ids)
            ).all()
        
        self.load_combinations = []
        if self.analysis.load_combination_ids:
            self.load_combinations = db.query(LoadCombination).filter(
                LoadCombination.id.in_(self.analysis.load_combination_ids)
            ).all()
        
        # Initialize matrices
        self.num_nodes = len(self.nodes)
        self.num_elements = len(self.elements)
        self.dof_per_node = 6  # 3 translations + 3 rotations
        self.total_dof = self.num_nodes * self.dof_per_node
        
        # Node and element mapping for easy access
        self.node_map = {node.id: i for i, node in enumerate(self.nodes)}
        self.element_map = {element.id: i for i, element in enumerate(self.elements)}
    
    def run_analysis(self) -> None:
        """
        Run the analysis based on the analysis type.
        """
        try:
            logger.info(f"Starting analysis {self.analysis.name} (ID: {self.analysis_id})")
            
            # Clear previous results
            self._clear_previous_results()
            
            # Run the appropriate analysis
            if self.analysis.analysis_type == AnalysisType.LINEAR_STATIC:
                self._run_linear_static_analysis()
            elif self.analysis.analysis_type == AnalysisType.NONLINEAR_STATIC:
                self._run_nonlinear_static_analysis()
            elif self.analysis.analysis_type == AnalysisType.MODAL:
                self._run_modal_analysis()
            elif self.analysis.analysis_type == AnalysisType.RESPONSE_SPECTRUM:
                self._run_response_spectrum_analysis()
            elif self.analysis.analysis_type == AnalysisType.TIME_HISTORY:
                self._run_time_history_analysis()
            elif self.analysis.analysis_type == AnalysisType.BUCKLING:
                self._run_buckling_analysis()
            elif self.analysis.analysis_type == AnalysisType.P_DELTA:
                self._run_p_delta_analysis()
            else:
                raise ValueError(f"Unsupported analysis type: {self.analysis.analysis_type}")
            
            # Update analysis status
            self.analysis.is_complete = True
            self.analysis.run_date = datetime.utcnow()
            self.db.commit()
            
            logger.info(f"Analysis {self.analysis.name} completed successfully")
        
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error running analysis {self.analysis.name}: {str(e)}")
            raise
    
    def _clear_previous_results(self) -> None:
        """
        Clear previous analysis results.
        """
        self.db.query(NodeResult).filter(NodeResult.analysis_id == self.analysis_id).delete()
        self.db.query(ElementResult).filter(ElementResult.analysis_id == self.analysis_id).delete()
        self.db.query(ModalResult).filter(ModalResult.analysis_id == self.analysis_id).delete()
        self.db.commit()
    
    def _run_linear_static_analysis(self) -> None:
        """
        Run linear static analysis.
        """
        # For each load case
        for load_case in self.load_cases:
            # 1. Assemble global stiffness matrix
            K_global = self._assemble_global_stiffness_matrix()
            
            # 2. Assemble load vector
            F_global = self._assemble_load_vector(load_case.id)
            
            # 3. Apply boundary conditions
            K_reduced, F_reduced, bc_data = self._apply_boundary_conditions(K_global, F_global)
            
            # 4. Solve the system of equations
            U_reduced = np.linalg.solve(K_reduced, F_reduced)
            
            # 5. Recover full displacement vector
            U_global = self._recover_full_displacement_vector(U_reduced, bc_data)
            
            # 6. Calculate element forces and stresses
            self._calculate_element_results(U_global, load_case.id)
            
            # 7. Store node results
            self._store_node_results(U_global, load_case.id)
        
        # For each load combination
        for load_combination in self.load_combinations:
            # Get load cases and factors
            combination_cases = self.db.query(LoadCombinationCase).filter(
                LoadCombinationCase.load_combination_id == load_combination.id
            ).all()
            
            # Combine results
            self._combine_results(load_combination.id, combination_cases)
    
    def _run_nonlinear_static_analysis(self) -> None:
        """
        Run nonlinear static analysis.
        """
        # Implementation for nonlinear static analysis
        pass
    
    def _run_modal_analysis(self) -> None:
        """
        Run modal analysis.
        """
        # 1. Assemble global stiffness matrix
        K_global = self._assemble_global_stiffness_matrix()
        
        # 2. Assemble global mass matrix
        M_global = self._assemble_global_mass_matrix()
        
        # 3. Apply boundary conditions
        K_reduced, M_reduced, bc_data = self._apply_boundary_conditions_modal(K_global, M_global)
        
        # 4. Solve the generalized eigenvalue problem
        eigenvalues, eigenvectors = self._solve_eigenvalue_problem(K_reduced, M_reduced)
        
        # 5. Store modal results
        self._store_modal_results(eigenvalues, eigenvectors, bc_data)
    
    def _run_response_spectrum_analysis(self) -> None:
        """
        Run response spectrum analysis.
        """
        # Implementation for response spectrum analysis
        pass
    
    def _run_time_history_analysis(self) -> None:
        """
        Run time history analysis.
        """
        # Implementation for time history analysis
        pass
    
    def _run_buckling_analysis(self) -> None:
        """
        Run buckling analysis.
        """
        # Implementation for buckling analysis
        pass
    
    def _run_p_delta_analysis(self) -> None:
        """
        Run P-Delta analysis.
        """
        # Implementation for P-Delta analysis
        pass
    
    def _assemble_global_stiffness_matrix(self) -> np.ndarray:
        """
        Assemble the global stiffness matrix.
        """
        # Initialize global stiffness matrix
        K_global = np.zeros((self.total_dof, self.total_dof))
        
        # For each element
        for element in self.elements:
            # Get element properties
            material = self.db.query(Material).filter(Material.id == element.material_id).first()
            section = self.db.query(Section).filter(Section.id == element.section_id).first()
            
            # Get element nodes
            start_node = self.db.query(Node).filter(Node.id == element.start_node_id).first()
            end_node = self.db.query(Node).filter(Node.id == element.end_node_id).first()
            
            # Calculate element length and direction cosines
            dx = end_node.x - start_node.x
            dy = end_node.y - start_node.y
            dz = end_node.z - start_node.z
            L = np.sqrt(dx**2 + dy**2 + dz**2)
            
            # Calculate element stiffness matrix in local coordinates
            K_local = self._calculate_element_stiffness_matrix(
                L, material.elastic_modulus, section.area, 
                section.moment_of_inertia_y, section.moment_of_inertia_z, 
                section.torsional_constant, material.poisson_ratio
            )
            
            # Transform to global coordinates
            T = self._calculate_transformation_matrix(dx, dy, dz, L, element.angle)
            K_element = T.T @ K_local @ T
            
            # Assemble into global stiffness matrix
            dof_indices = self._get_element_dof_indices(element)
            for i, row in enumerate(dof_indices):
                for j, col in enumerate(dof_indices):
                    K_global[row, col] += K_element[i, j]
        
        return K_global
    
    def _assemble_global_mass_matrix(self) -> np.ndarray:
        """
        Assemble the global mass matrix.
        """
        # Initialize global mass matrix
        M_global = np.zeros((self.total_dof, self.total_dof))
        
        # For each element
        for element in self.elements:
            # Get element properties
            material = self.db.query(Material).filter(Material.id == element.material_id).first()
            section = self.db.query(Section).filter(Section.id == element.section_id).first()
            
            # Get element nodes
            start_node = self.db.query(Node).filter(Node.id == element.start_node_id).first()
            end_node = self.db.query(Node).filter(Node.id == element.end_node_id).first()
            
            # Calculate element length
            dx = end_node.x - start_node.x
            dy = end_node.y - start_node.y
            dz = end_node.z - start_node.z
            L = np.sqrt(dx**2 + dy**2 + dz**2)
            
            # Calculate element mass matrix in local coordinates
            M_local = self._calculate_element_mass_matrix(
                L, material.density, section.area
            )
            
            # Transform to global coordinates
            T = self._calculate_transformation_matrix(dx, dy, dz, L, element.angle)
            M_element = T.T @ M_local @ T
            
            # Assemble into global mass matrix
            dof_indices = self._get_element_dof_indices(element)
            for i, row in enumerate(dof_indices):
                for j, col in enumerate(dof_indices):
                    M_global[row, col] += M_element[i, j]
        
        return M_global
    
    def _assemble_load_vector(self, load_case_id: str) -> np.ndarray:
        """
        Assemble the load vector for a given load case.
        """
        # Initialize load vector
        F_global = np.zeros(self.total_dof)
        
        # Get loads for this load case
        loads = self.db.query(Load).filter(
            Load.load_case_id == load_case_id,
            Load.project_id == self.project_id
        ).all()
        
        # Process nodal loads
        for load in loads:
            if load.node_id:
                node_index = self.node_map.get(load.node_id)
                if node_index is not None:
                    dof_start = node_index * self.dof_per_node
                    
                    # Apply forces
                    if load.fx is not None:
                        F_global[dof_start] += load.fx
                    if load.fy is not None:
                        F_global[dof_start + 1] += load.fy
                    if load.fz is not None:
                        F_global[dof_start + 2] += load.fz
                    
                    # Apply moments
                    if load.mx is not None:
                        F_global[dof_start + 3] += load.mx
                    if load.my is not None:
                        F_global[dof_start + 4] += load.my
                    if load.mz is not None:
                        F_global[dof_start + 5] += load.mz
            
            # Process element loads (distributed, etc.)
            elif load.element_id:
                # Implementation for element loads
                pass
        
        return F_global
    
    def _apply_boundary_conditions(
        self, K_global: np.ndarray, F_global: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray, Dict[str, Any]]:
        """
        Apply boundary conditions to the global stiffness matrix and load vector.
        """
        # Identify constrained DOFs
        constrained_dofs = []
        for i, node in enumerate(self.nodes):
            if node.is_support:
                dof_start = i * self.dof_per_node
                
                # Check each DOF constraint
                if node.restraint_x:
                    constrained_dofs.append(dof_start)
                if node.restraint_y:
                    constrained_dofs.append(dof_start + 1)
                if node.restraint_z:
                    constrained_dofs.append(dof_start + 2)
                if node.restraint_rx:
                    constrained_dofs.append(dof_start + 3)
                if node.restraint_ry:
                    constrained_dofs.append(dof_start + 4)
                if node.restraint_rz:
                    constrained_dofs.append(dof_start + 5)
        
        # Get free DOFs
        all_dofs = set(range(self.total_dof))
        free_dofs = list(all_dofs - set(constrained_dofs))
        
        # Reduce matrices
        K_reduced = K_global[np.ix_(free_dofs, free_dofs)]
        F_reduced = F_global[free_dofs]
        
        # Store boundary condition data for recovery
        bc_data = {
            "free_dofs": free_dofs,
            "constrained_dofs": constrained_dofs
        }
        
        return K_reduced, F_reduced, bc_data
    
    def _apply_boundary_conditions_modal(
        self, K_global: np.ndarray, M_global: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray, Dict[str, Any]]:
        """
        Apply boundary conditions for modal analysis.
        """
        # Identify constrained DOFs (similar to _apply_boundary_conditions)
        constrained_dofs = []
        for i, node in enumerate(self.nodes):
            if node.is_support:
                dof_start = i * self.dof_per_node
                
                # Check each DOF constraint
                if node.restraint_x:
                    constrained_dofs.append(dof_start)
                if node.restraint_y:
                    constrained_dofs.append(dof_start + 1)
                if node.restraint_z:
                    constrained_dofs.append(dof_start + 2)
                if node.restraint_rx:
                    constrained_dofs.append(dof_start + 3)
                if node.restraint_ry:
                    constrained_dofs.append(dof_start + 4)
                if node.restraint_rz:
                    constrained_dofs.append(dof_start + 5)
        
        # Get free DOFs
        all_dofs = set(range(self.total_dof))
        free_dofs = list(all_dofs - set(constrained_dofs))
        
        # Reduce matrices
        K_reduced = K_global[np.ix_(free_dofs, free_dofs)]
        M_reduced = M_global[np.ix_(free_dofs, free_dofs)]
        
        # Store boundary condition data for recovery
        bc_data = {
            "free_dofs": free_dofs,
            "constrained_dofs": constrained_dofs
        }
        
        return K_reduced, M_reduced, bc_data
    
    def _recover_full_displacement_vector(
        self, U_reduced: np.ndarray, bc_data: Dict[str, Any]
    ) -> np.ndarray:
        """
        Recover the full displacement vector from the reduced solution.
        """
        # Initialize full displacement vector with zeros
        U_global = np.zeros(self.total_dof)
        
        # Fill in the computed displacements
        for i, dof in enumerate(bc_data["free_dofs"]):
            U_global[dof] = U_reduced[i]
        
        return U_global
    
    def _calculate_element_results(
        self, U_global: np.ndarray, load_case_id: Optional[str] = None, load_combination_id: Optional[str] = None
    ) -> None:
        """
        Calculate element forces and stresses from the displacement vector.
        """
        # For each element
        for element in self.elements:
            # Get element properties
            material = self.db.query(Material).filter(Material.id == element.material_id).first()
            section = self.db.query(Section).filter(Section.id == element.section_id).first()
            
            # Get element nodes
            start_node = self.db.query(Node).filter(Node.id == element.start_node_id).first()
            end_node = self.db.query(Node).filter(Node.id == element.end_node_id).first()
            
            # Calculate element length and direction cosines
            dx = end_node.x - start_node.x
            dy = end_node.y - start_node.y
            dz = end_node.z - start_node.z
            L = np.sqrt(dx**2 + dy**2 + dz**2)
            
            # Get element DOF indices
            dof_indices = self._get_element_dof_indices(element)
            
            # Extract element displacements
            U_element = U_global[dof_indices]
            
            # Transform to local coordinates
            T = self._calculate_transformation_matrix(dx, dy, dz, L, element.angle)
            U_local = T @ U_element
            
            # Calculate element forces in local coordinates
            K_local = self._calculate_element_stiffness_matrix(
                L, material.elastic_modulus, section.area, 
                section.moment_of_inertia_y, section.moment_of_inertia_z, 
                section.torsional_constant, material.poisson_ratio
            )
            F_local = K_local @ U_local
            
            # Calculate stresses
            axial_force = F_local[0]  # Axial force at start node
            shear_force_y = F_local[1]  # Shear force in y direction at start node
            shear_force_z = F_local[2]  # Shear force in z direction at start node
            torsional_moment = F_local[3]  # Torsional moment at start node
            bending_moment_y = F_local[4]  # Bending moment about y axis at start node
            bending_moment_z = F_local[5]  # Bending moment about z axis at start node
            
            # Calculate stresses
            axial_stress = axial_force / section.area
            bending_stress_y = bending_moment_y / section.elastic_modulus_y
            bending_stress_z = bending_moment_z / section.elastic_modulus_z
            
            # Store results at start of element (position = 0.0)
            element_result_start = ElementResult(
                analysis_id=self.analysis_id,
                element_id=element.id,
                load_case_id=load_case_id,
                load_combination_id=load_combination_id,
                position=0.0,
                axial_force=axial_force,
                shear_force_y=shear_force_y,
                shear_force_z=shear_force_z,
                torsional_moment=torsional_moment,
                bending_moment_y=bending_moment_y,
                bending_moment_z=bending_moment_z,
                axial_stress=axial_stress,
                bending_stress_y=bending_stress_y,
                bending_stress_z=bending_stress_z,
                von_mises_stress=np.sqrt(axial_stress**2 + 3 * (bending_stress_y**2 + bending_stress_z**2))
            )
            self.db.add(element_result_start)
            
            # Calculate and store results at end of element (position = 1.0)
            # Note: For a beam element, the end forces are related to the start forces
            axial_force_end = -F_local[6]  # Axial force at end node
            shear_force_y_end = -F_local[7]  # Shear force in y direction at end node
            shear_force_z_end = -F_local[8]  # Shear force in z direction at end node
            torsional_moment_end = -F_local[9]  # Torsional moment at end node
            bending_moment_y_end = -F_local[10]  # Bending moment about y axis at end node
            bending_moment_z_end = -F_local[11]  # Bending moment about z axis at end node
            
            # Calculate stresses at end
            axial_stress_end = axial_force_end / section.area
            bending_stress_y_end = bending_moment_y_end / section.elastic_modulus_y
            bending_stress_z_end = bending_moment_z_end / section.elastic_modulus_z
            
            element_result_end = ElementResult(
                analysis_id=self.analysis_id,
                element_id=element.id,
                load_case_id=load_case_id,
                load_combination_id=load_combination_id,
                position=1.0,
                axial_force=axial_force_end,
                shear_force_y=shear_force_y_end,
                shear_force_z=shear_force_z_end,
                torsional_moment=torsional_moment_end,
                bending_moment_y=bending_moment_y_end,
                bending_moment_z=bending_moment_z_end,
                axial_stress=axial_stress_end,
                bending_stress_y=bending_stress_y_end,
                bending_stress_z=bending_stress_z_end,
                von_mises_stress=np.sqrt(axial_stress_end**2 + 3 * (bending_stress_y_end**2 + bending_stress_z_end**2))
            )
            self.db.add(element_result_end)
            
            # Optionally, calculate and store results at midpoint (position = 0.5)
            # This would require interpolation of the results
            
            self.db.commit()
    
    def _store_node_results(
        self, U_global: np.ndarray, load_case_id: Optional[str] = None, load_combination_id: Optional[str] = None
    ) -> None:
        """
        Store node displacements and reactions.
        """
        # For each node
        for i, node in enumerate(self.nodes):
            dof_start = i * self.dof_per_node
            
            # Extract displacements
            dx = U_global[dof_start]
            dy = U_global[dof_start + 1]
            dz = U_global[dof_start + 2]
            rx = U_global[dof_start + 3]
            ry = U_global[dof_start + 4]
            rz = U_global[dof_start + 5]
            
            # For support nodes, calculate reactions
            fx, fy, fz, mx, my, mz = None, None, None, None, None, None
            if node.is_support:
                # Reactions are calculated from the global stiffness matrix and displacements
                # This is a simplified approach; in practice, you would use the element forces
                pass
            
            # Store node result
            node_result = NodeResult(
                analysis_id=self.analysis_id,
                node_id=node.id,
                load_case_id=load_case_id,
                load_combination_id=load_combination_id,
                dx=dx,
                dy=dy,
                dz=dz,
                rx=rx,
                ry=ry,
                rz=rz,
                fx=fx,
                fy=fy,
                fz=fz,
                mx=mx,
                my=my,
                mz=mz
            )
            self.db.add(node_result)
        
        self.db.commit()
    
    def _combine_results(
        self, load_combination_id: str, combination_cases: List[LoadCombinationCase]
    ) -> None:
        """
        Combine results from multiple load cases according to load combination factors.
        """
        # Get all nodes and elements
        nodes = self.db.query(Node).filter(Node.project_id == self.project_id).all()
        elements = self.db.query(Element).filter(Element.project_id == self.project_id).all()
        
        # For each node
        for node in nodes:
            # Initialize combined results
            dx, dy, dz = 0.0, 0.0, 0.0
            rx, ry, rz = 0.0, 0.0, 0.0
            fx, fy, fz = 0.0, 0.0, 0.0
            mx, my, mz = 0.0, 0.0, 0.0
            
            # Combine results from each load case
            for case in combination_cases:
                # Get node result for this load case
                node_result = self.db.query(NodeResult).filter(
                    NodeResult.analysis_id == self.analysis_id,
                    NodeResult.node_id == node.id,
                    NodeResult.load_case_id == case.load_case_id
                ).first()
                
                if node_result:
                    # Apply load factor
                    factor = case.factor
                    
                    # Add to combined results
                    if node_result.dx is not None:
                        dx += node_result.dx * factor
                    if node_result.dy is not None:
                        dy += node_result.dy * factor
                    if node_result.dz is not None:
                        dz += node_result.dz * factor
                    if node_result.rx is not None:
                        rx += node_result.rx * factor
                    if node_result.ry is not None:
                        ry += node_result.ry * factor
                    if node_result.rz is not None:
                        rz += node_result.rz * factor
                    
                    # Reactions
                    if node_result.fx is not None:
                        fx += node_result.fx * factor
                    if node_result.fy is not None:
                        fy += node_result.fy * factor
                    if node_result.fz is not None:
                        fz += node_result.fz * factor
                    if node_result.mx is not None:
                        mx += node_result.mx * factor
                    if node_result.my is not None:
                        my += node_result.my * factor
                    if node_result.mz is not None:
                        mz += node_result.mz * factor
            
            # Store combined node result
            combined_node_result = NodeResult(
                analysis_id=self.analysis_id,
                node_id=node.id,
                load_combination_id=load_combination_id,
                dx=dx,
                dy=dy,
                dz=dz,
                rx=rx,
                ry=ry,
                rz=rz,
                fx=fx if node.is_support else None,
                fy=fy if node.is_support else None,
                fz=fz if node.is_support else None,
                mx=mx if node.is_support else None,
                my=my if node.is_support else None,
                mz=mz if node.is_support else None
            )
            self.db.add(combined_node_result)
        
        # For each element and position (0.0 and 1.0)
        for element in elements:
            for position in [0.0, 1.0]:
                # Initialize combined results
                axial_force, shear_force_y, shear_force_z = 0.0, 0.0, 0.0
                torsional_moment, bending_moment_y, bending_moment_z = 0.0, 0.0, 0.0
                axial_stress, bending_stress_y, bending_stress_z = 0.0, 0.0, 0.0
                von_mises_stress = 0.0
                
                # Combine results from each load case
                for case in combination_cases:
                    # Get element result for this load case and position
                    element_result = self.db.query(ElementResult).filter(
                        ElementResult.analysis_id == self.analysis_id,
                        ElementResult.element_id == element.id,
                        ElementResult.load_case_id == case.load_case_id,
                        ElementResult.position == position
                    ).first()
                    
                    if element_result:
                        # Apply load factor
                        factor = case.factor
                        
                        # Add to combined results
                        if element_result.axial_force is not None:
                            axial_force += element_result.axial_force * factor
                        if element_result.shear_force_y is not None:
                            shear_force_y += element_result.shear_force_y * factor
                        if element_result.shear_force_z is not None:
                            shear_force_z += element_result.shear_force_z * factor
                        if element_result.torsional_moment is not None:
                            torsional_moment += element_result.torsional_moment * factor
                        if element_result.bending_moment_y is not None:
                            bending_moment_y += element_result.bending_moment_y * factor
                        if element_result.bending_moment_z is not None:
                            bending_moment_z += element_result.bending_moment_z * factor
                
                # Calculate stresses
                section = self.db.query(Section).filter(Section.id == element.section_id).first()
                if section:
                    axial_stress = axial_force / section.area
                    bending_stress_y = bending_moment_y / section.elastic_modulus_y
                    bending_stress_z = bending_moment_z / section.elastic_modulus_z
                    von_mises_stress = np.sqrt(axial_stress**2 + 3 * (bending_stress_y**2 + bending_stress_z**2))
                
                # Store combined element result
                combined_element_result = ElementResult(
                    analysis_id=self.analysis_id,
                    element_id=element.id,
                    load_combination_id=load_combination_id,
                    position=position,
                    axial_force=axial_force,
                    shear_force_y=shear_force_y,
                    shear_force_z=shear_force_z,
                    torsional_moment=torsional_moment,
                    bending_moment_y=bending_moment_y,
                    bending_moment_z=bending_moment_z,
                    axial_stress=axial_stress,
                    bending_stress_y=bending_stress_y,
                    bending_stress_z=bending_stress_z,
                    von_mises_stress=von_mises_stress
                )
                self.db.add(combined_element_result)
        
        self.db.commit()
    
    def _solve_eigenvalue_problem(
        self, K: np.ndarray, M: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Solve the generalized eigenvalue problem for modal analysis.
        """
        # Solve the generalized eigenvalue problem: K*v = lambda*M*v
        eigenvalues, eigenvectors = np.linalg.eig(np.linalg.inv(M) @ K)
        
        # Sort by eigenvalues (frequencies)
        idx = eigenvalues.argsort()
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
        
        return eigenvalues, eigenvectors
    
    def _store_modal_results(
        self, eigenvalues: np.ndarray, eigenvectors: np.ndarray, bc_data: Dict[str, Any]
    ) -> None:
        """
        Store modal analysis results.
        """
        # Number of modes to store
        num_modes = min(len(eigenvalues), self.analysis.num_modes or 10)
        
        # For each mode
        for i in range(num_modes):
            # Calculate frequency and period
            omega = np.sqrt(eigenvalues[i])  # rad/s
            frequency = omega / (2 * np.pi)  # Hz
            period = 1 / frequency  # s
            
            # Recover full mode shape
            mode_shape_reduced = eigenvectors[:, i]
            mode_shape_full = np.zeros(self.total_dof)
            for j, dof in enumerate(bc_data["free_dofs"]):
                mode_shape_full[dof] = mode_shape_reduced[j]
            
            # Calculate modal mass and participation factors
            # This is a simplified approach
            modal_mass = 1.0  # Normalized
            participation_x = 0.0
            participation_y = 0.0
            participation_z = 0.0
            participation_rx = 0.0
            participation_ry = 0.0
            participation_rz = 0.0
            
            # Store mode shape as JSON
            mode_shape_json = {}
            for j, node in enumerate(self.nodes):
                dof_start = j * self.dof_per_node
                mode_shape_json[node.id] = [
                    float(mode_shape_full[dof_start]),      # dx
                    float(mode_shape_full[dof_start + 1]),  # dy
                    float(mode_shape_full[dof_start + 2]),  # dz
                    float(mode_shape_full[dof_start + 3]),  # rx
                    float(mode_shape_full[dof_start + 4]),  # ry
                    float(mode_shape_full[dof_start + 5])   # rz
                ]
            
            # Store modal result
            modal_result = ModalResult(
                analysis_id=self.analysis_id,
                mode_number=i + 1,
                frequency=float(frequency),
                period=float(period),
                modal_mass=modal_mass,
                participation_x=participation_x,
                participation_y=participation_y,
                participation_z=participation_z,
                participation_rx=participation_rx,
                participation_ry=participation_ry,
                participation_rz=participation_rz,
                mode_shape=mode_shape_json
            )
            self.db.add(modal_result)
        
        self.db.commit()
    
    def _get_element_dof_indices(self, element: Element) -> List[int]:
        """
        Get the global DOF indices for an element.
        """
        start_node_index = self.node_map.get(element.start_node_id)
        end_node_index = self.node_map.get(element.end_node_id)
        
        start_dof = start_node_index * self.dof_per_node
        end_dof = end_node_index * self.dof_per_node
        
        return [
            start_dof, start_dof + 1, start_dof + 2, start_dof + 3, start_dof + 4, start_dof + 5,
            end_dof, end_dof + 1, end_dof + 2, end_dof + 3, end_dof + 4, end_dof + 5
        ]
    
    def _calculate_element_stiffness_matrix(
        self, L: float, E: float, A: float, Iy: float, Iz: float, J: float, nu: float
    ) -> np.ndarray:
        """
        Calculate the element stiffness matrix in local coordinates.
        """
        # Simplified 3D beam element stiffness matrix
        # This is a placeholder and should be replaced with a proper implementation
        G = E / (2 * (1 + nu))  # Shear modulus
        
        # Initialize stiffness matrix
        K = np.zeros((12, 12))
        
        # Axial terms
        K[0, 0] = K[6, 6] = E * A / L
        K[0, 6] = K[6, 0] = -E * A / L
        
        # Torsional terms
        K[3, 3] = K[9, 9] = G * J / L
        K[3, 9] = K[9, 3] = -G * J / L
        
        # Bending terms (y-axis)
        K[1, 1] = K[7, 7] = 12 * E * Iz / L**3
        K[1, 7] = K[7, 1] = -12 * E * Iz / L**3
        K[1, 5] = K[5, 1] = 6 * E * Iz / L**2
        K[1, 11] = K[11, 1] = 6 * E * Iz / L**2
        K[5, 5] = K[11, 11] = 4 * E * Iz / L
        K[5, 7] = K[7, 5] = -6 * E * Iz / L**2
        K[5, 11] = K[11, 5] = 2 * E * Iz / L
        K[7, 11] = K[11, 7] = -6 * E * Iz / L**2
        
        # Bending terms (z-axis)
        K[2, 2] = K[8, 8] = 12 * E * Iy / L**3
        K[2, 8] = K[8, 2] = -12 * E * Iy / L**3
        K[2, 4] = K[4, 2] = -6 * E * Iy / L**2
        K[2, 10] = K[10, 2] = -6 * E * Iy / L**2
        K[4, 4] = K[10, 10] = 4 * E * Iy / L
        K[4, 8] = K[8, 4] = 6 * E * Iy / L**2
        K[4, 10] = K[10, 4] = 2 * E * Iy / L
        K[8, 10] = K[10, 8] = 6 * E * Iy / L**2
        
        return K
    
    def _calculate_element_mass_matrix(
        self, L: float, rho: float, A: float
    ) -> np.ndarray:
        """
        Calculate the element mass matrix in local coordinates.
        """
        # Simplified consistent mass matrix for a 3D beam element
        # This is a placeholder and should be replaced with a proper implementation
        m = rho * A * L  # Total mass of the element
        
        # Initialize mass matrix
        M = np.zeros((12, 12))
        
        # Translational terms
        M[0, 0] = M[6, 6] = m / 3
        M[0, 6] = M[6, 0] = m / 6
        
        M[1, 1] = M[7, 7] = m / 3
        M[1, 7] = M[7, 1] = m / 6
        
        M[2, 2] = M[8, 8] = m / 3
        M[2, 8] = M[8, 2] = m / 6
        
        # Rotational terms (simplified)
        M[3, 3] = M[9, 9] = m * L**2 / 3
        M[3, 9] = M[9, 3] = m * L**2 / 6
        
        M[4, 4] = M[10, 10] = m * L**2 / 3
        M[4, 10] = M[10, 4] = m * L**2 / 6
        
        M[5, 5] = M[11, 11] = m * L**2 / 3
        M[5, 11] = M[11, 5] = m * L**2 / 6
        
        return M
    
    def _calculate_transformation_matrix(
        self, dx: float, dy: float, dz: float, L: float, angle: float
    ) -> np.ndarray:
        """
        Calculate the transformation matrix from local to global coordinates.
        """
        # Direction cosines
        if L < 1e-10:  # Avoid division by zero
            L = 1e-10
        
        cx = dx / L
        cy = dy / L
        cz = dz / L
        
        # Handle special case of vertical element
        if abs(cx) < 1e-10 and abs(cy) < 1e-10:
            # Element is vertical, use a different approach
            cx_p = 1.0
            cy_p = 0.0
            cz_p = 0.0
        else:
            # Normal case
            # Calculate perpendicular direction
            d = np.sqrt(cx**2 + cy**2)
            cx_p = -cy / d
            cy_p = cx / d
            cz_p = 0.0
        
        # Apply rotation angle
        angle_rad = np.radians(angle)
        cos_a = np.cos(angle_rad)
        sin_a = np.sin(angle_rad)
        
        cx_pp = cx_p * cos_a + (cy * cz_p - cz * cy_p) * sin_a
        cy_pp = cy_p * cos_a + (cz * cx_p - cx * cz_p) * sin_a
        cz_pp = cz_p * cos_a + (cx * cy_p - cy * cx_p) * sin_a
        
        # Create 3x3 rotation matrix
        R = np.array([
            [cx, cy, cz],
            [cx_pp, cy_pp, cz_pp],
            [cy * cz_pp - cz * cy_pp, cz * cx_pp - cx * cz_pp, cx * cy_pp - cy * cx_pp]
        ])
        
        # Create 12x12 transformation matrix
        T = np.zeros((12, 12))
        for i in range(4):
            T[3*i:3*i+3, 3*i:3*i+3] = R
        
        return T


def run_analysis_task(db: Session, analysis_id: str) -> None:
    """
    Run an analysis task.
    """
    try:
        # Create solver
        solver = StructuralAnalysisSolver(db, analysis_id)
        
        # Run analysis
        solver.run_analysis()
    
    except Exception as e:
        logger.error(f"Error running analysis task: {str(e)}")
        # Update analysis status to indicate failure
        analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if analysis:
            analysis.is_complete = False
            db.commit()