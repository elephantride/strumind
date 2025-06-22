import asyncio
import os
import time
from playwright.async_api import async_playwright

# Configuration
API_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:5173"
RECORDING_PATH = os.path.join(os.path.dirname(__file__), "recordings")

# Ensure recording directory exists
os.makedirs(RECORDING_PATH, exist_ok=True)

async def test_10_story_building():
    """
    Test the full workflow of designing a 10-story building:
    1. Define the structural model
    2. Run analysis (linear static, P-delta, dynamic)
    3. Perform design checks
    4. Generate detailing data
    5. Visualize 3D BIM model
    """
    async with async_playwright() as p:
        # Launch browser with video recording
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            record_video_dir=RECORDING_PATH,
            viewport={"width": 1920, "height": 1080}
        )
        page = await context.new_page()
        
        # Navigate to the frontend
        await page.goto(FRONTEND_URL)
        await page.wait_for_load_state("networkidle")
        
        # Step 1: Create a new project
        print("Creating a new project...")
        await page.click("text=New Project")
        await page.fill("input[placeholder='Project Name']", "10-Story Building")
        await page.fill("textarea[placeholder='Description']", "Test of a 10-story steel frame building")
        await page.click("text=Create Project")
        await page.wait_for_selector("text=Project created successfully")
        
        # Step 2: Define materials
        print("Defining materials...")
        await page.click("text=Materials")
        await page.click("text=Add Material")
        await page.fill("input[placeholder='Material Name']", "Structural Steel")
        await page.select_option("select[name='material_type']", "steel")
        await page.fill("input[name='density']", "7850")
        await page.fill("input[name='elastic_modulus']", "200000")
        await page.fill("input[name='poisson_ratio']", "0.3")
        await page.fill("input[name='yield_strength']", "345")
        await page.fill("input[name='ultimate_strength']", "450")
        await page.click("text=Save Material")
        await page.wait_for_selector("text=Material created successfully")
        
        # Step 3: Define sections
        print("Defining sections...")
        await page.click("text=Sections")
        await page.click("text=Add Section")
        await page.fill("input[placeholder='Section Name']", "W14x90")
        await page.select_option("select[name='section_type']", "i_section")
        # Select the material we just created
        await page.select_option("select[name='material_id']", "Structural Steel")
        # Fill section properties
        await page.fill("input[name='area']", "17100")
        await page.fill("input[name='moment_of_inertia_y']", "999000000")
        await page.fill("input[name='moment_of_inertia_z']", "339000000")
        await page.fill("input[name='torsional_constant']", "15700000")
        await page.fill("input[name='elastic_modulus_y']", "1380000")
        await page.fill("input[name='elastic_modulus_z']", "677000")
        await page.fill("input[name='plastic_modulus_y']", "1560000")
        await page.fill("input[name='plastic_modulus_z']", "1040000")
        # Add dimensions as JSON
        await page.fill("textarea[name='dimensions']", '{"h": 368, "b": 256, "tw": 15, "tf": 23}')
        await page.click("text=Save Section")
        await page.wait_for_selector("text=Section created successfully")
        
        # Add column section
        await page.click("text=Add Section")
        await page.fill("input[placeholder='Section Name']", "W14x120")
        await page.select_option("select[name='section_type']", "i_section")
        await page.select_option("select[name='material_id']", "Structural Steel")
        await page.fill("input[name='area']", "22800")
        await page.fill("input[name='moment_of_inertia_y']", "1380000000")
        await page.fill("input[name='moment_of_inertia_z']", "471000000")
        await page.fill("input[name='torsional_constant']", "23700000")
        await page.fill("input[name='elastic_modulus_y']", "1910000")
        await page.fill("input[name='elastic_modulus_z']", "940000")
        await page.fill("input[name='plastic_modulus_y']", "2170000")
        await page.fill("input[name='plastic_modulus_z']", "1440000")
        await page.fill("textarea[name='dimensions']", '{"h": 373, "b": 373, "tw": 16, "tf": 26}')
        await page.click("text=Save Section")
        await page.wait_for_selector("text=Section created successfully")
        
        # Step 4: Define nodes for a 10-story building
        print("Defining nodes...")
        await page.click("text=Nodes")
        
        # Create a grid of nodes for a 10-story building
        # We'll create a 3x3 grid in plan, with 10 stories
        grid_spacing = 6.0  # 6 meters
        story_height = 3.5  # 3.5 meters
        
        # Create nodes
        for story in range(11):  # 0 to 10 (ground + 10 stories)
            z = story * story_height
            for x in range(3):
                for y in range(3):
                    await page.click("text=Add Node")
                    node_name = f"N{story}-{x}-{y}"
                    await page.fill("input[placeholder='Node Name']", node_name)
                    await page.fill("input[name='x']", str(x * grid_spacing))
                    await page.fill("input[name='y']", str(y * grid_spacing))
                    await page.fill("input[name='z']", str(z))
                    
                    # Add support conditions for ground floor
                    if story == 0:
                        await page.check("input[name='is_support']")
                        await page.check("input[name='restraint_x']")
                        await page.check("input[name='restraint_y']")
                        await page.check("input[name='restraint_z']")
                        await page.check("input[name='restraint_rx']")
                        await page.check("input[name='restraint_ry']")
                        await page.check("input[name='restraint_rz']")
                    
                    await page.click("text=Save Node")
                    await page.wait_for_selector("text=Node created successfully")
        
        # Step 5: Define elements (columns and beams)
        print("Defining elements...")
        await page.click("text=Elements")
        
        # Create columns
        for story in range(10):  # 0 to 9 (connecting to story above)
            for x in range(3):
                for y in range(3):
                    await page.click("text=Add Element")
                    element_name = f"C{story}-{x}-{y}"
                    await page.fill("input[placeholder='Element Name']", element_name)
                    await page.select_option("select[name='element_type']", "column")
                    
                    # Select start and end nodes
                    start_node = f"N{story}-{x}-{y}"
                    end_node = f"N{story+1}-{x}-{y}"
                    await page.select_option("select[name='start_node_id']", start_node)
                    await page.select_option("select[name='end_node_id']", end_node)
                    
                    # Select section and material
                    await page.select_option("select[name='section_id']", "W14x120")
                    await page.select_option("select[name='material_id']", "Structural Steel")
                    
                    await page.click("text=Save Element")
                    await page.wait_for_selector("text=Element created successfully")
        
        # Create beams in X direction
        for story in range(1, 11):  # 1 to 10 (all elevated floors)
            for x in range(2):  # 0 to 1 (connecting to next x)
                for y in range(3):
                    await page.click("text=Add Element")
                    element_name = f"BX{story}-{x}-{y}"
                    await page.fill("input[placeholder='Element Name']", element_name)
                    await page.select_option("select[name='element_type']", "beam")
                    
                    # Select start and end nodes
                    start_node = f"N{story}-{x}-{y}"
                    end_node = f"N{story}-{x+1}-{y}"
                    await page.select_option("select[name='start_node_id']", start_node)
                    await page.select_option("select[name='end_node_id']", end_node)
                    
                    # Select section and material
                    await page.select_option("select[name='section_id']", "W14x90")
                    await page.select_option("select[name='material_id']", "Structural Steel")
                    
                    await page.click("text=Save Element")
                    await page.wait_for_selector("text=Element created successfully")
        
        # Create beams in Y direction
        for story in range(1, 11):  # 1 to 10 (all elevated floors)
            for x in range(3):
                for y in range(2):  # 0 to 1 (connecting to next y)
                    await page.click("text=Add Element")
                    element_name = f"BY{story}-{x}-{y}"
                    await page.fill("input[placeholder='Element Name']", element_name)
                    await page.select_option("select[name='element_type']", "beam")
                    
                    # Select start and end nodes
                    start_node = f"N{story}-{x}-{y}"
                    end_node = f"N{story}-{x}-{y+1}"
                    await page.select_option("select[name='start_node_id']", start_node)
                    await page.select_option("select[name='end_node_id']", end_node)
                    
                    # Select section and material
                    await page.select_option("select[name='section_id']", "W14x90")
                    await page.select_option("select[name='material_id']", "Structural Steel")
                    
                    await page.click("text=Save Element")
                    await page.wait_for_selector("text=Element created successfully")
        
        # Step 6: Define loads
        print("Defining loads...")
        await page.click("text=Loads")
        
        # Create load case
        await page.click("text=Add Load Case")
        await page.fill("input[placeholder='Load Case Name']", "Dead Load")
        await page.fill("textarea[placeholder='Description']", "Self-weight and superimposed dead load")
        await page.click("text=Save Load Case")
        await page.wait_for_selector("text=Load Case created successfully")
        
        await page.click("text=Add Load Case")
        await page.fill("input[placeholder='Load Case Name']", "Live Load")
        await page.fill("textarea[placeholder='Description']", "Office live load")
        await page.click("text=Save Load Case")
        await page.wait_for_selector("text=Load Case created successfully")
        
        await page.click("text=Add Load Case")
        await page.fill("input[placeholder='Load Case Name']", "Wind Load X")
        await page.fill("textarea[placeholder='Description']", "Wind load in X direction")
        await page.click("text=Save Load Case")
        await page.wait_for_selector("text=Load Case created successfully")
        
        # Add loads to beams
        # For simplicity, we'll add uniform loads to all beams
        await page.click("text=Add Load")
        await page.select_option("select[name='load_case_id']", "Dead Load")
        await page.select_option("select[name='load_type']", "distributed")
        
        # Select a beam element (we'll apply to all beams later)
        await page.select_option("select[name='element_id']", "BX1-0-0")
        
        # Add distributed load
        await page.fill("input[name='fz']", "-5000")  # -5 kN/m (downward)
        await page.fill("input[name='start_distance']", "0")
        await page.fill("input[name='end_distance']", "6")  # 6m (full length)
        
        await page.click("text=Save Load")
        await page.wait_for_selector("text=Load created successfully")
        
        # Add live load
        await page.click("text=Add Load")
        await page.select_option("select[name='load_case_id']", "Live Load")
        await page.select_option("select[name='load_type']", "distributed")
        await page.select_option("select[name='element_id']", "BX1-0-0")
        await page.fill("input[name='fz']", "-3000")  # -3 kN/m (downward)
        await page.fill("input[name='start_distance']", "0")
        await page.fill("input[name='end_distance']", "6")  # 6m (full length)
        await page.click("text=Save Load")
        await page.wait_for_selector("text=Load created successfully")
        
        # Add wind load (nodal loads at each story)
        for story in range(1, 11):
            await page.click("text=Add Load")
            await page.select_option("select[name='load_case_id']", "Wind Load X")
            await page.select_option("select[name='load_type']", "point")
            
            # Apply to corner node
            await page.select_option("select[name='node_id']", f"N{story}-0-0")
            
            # Force in X direction, increasing with height
            force = 5000 * (story / 10)  # 0.5 to 5 kN
            await page.fill("input[name='fx']", str(force))
            
            await page.click("text=Save Load")
            await page.wait_for_selector("text=Load created successfully")
        
        # Create load combinations
        await page.click("text=Add Load Combination")
        await page.fill("input[placeholder='Combination Name']", "1.2D + 1.6L")
        await page.fill("textarea[placeholder='Description']", "Strength design combination")
        
        # Add load cases to combination
        await page.click("text=Add Load Case")
        await page.select_option("select[name='load_case_id']", "Dead Load")
        await page.fill("input[name='factor']", "1.2")
        await page.click("text=Add")
        
        await page.click("text=Add Load Case")
        await page.select_option("select[name='load_case_id']", "Live Load")
        await page.fill("input[name='factor']", "1.6")
        await page.click("text=Add")
        
        await page.click("text=Save Combination")
        await page.wait_for_selector("text=Load Combination created successfully")
        
        # Wind load combination
        await page.click("text=Add Load Combination")
        await page.fill("input[placeholder='Combination Name']", "1.2D + 1.0W")
        await page.fill("textarea[placeholder='Description']", "Wind load combination")
        
        await page.click("text=Add Load Case")
        await page.select_option("select[name='load_case_id']", "Dead Load")
        await page.fill("input[name='factor']", "1.2")
        await page.click("text=Add")
        
        await page.click("text=Add Load Case")
        await page.select_option("select[name='load_case_id']", "Wind Load X")
        await page.fill("input[name='factor']", "1.0")
        await page.click("text=Add")
        
        await page.click("text=Save Combination")
        await page.wait_for_selector("text=Load Combination created successfully")
        
        # Step 7: Run analysis
        print("Running analysis...")
        await page.click("text=Analysis")
        
        # Create linear static analysis
        await page.click("text=New Analysis")
        await page.fill("input[placeholder='Analysis Name']", "Linear Static Analysis")
        await page.select_option("select[name='analysis_type']", "linear_static")
        
        # Select load combinations
        await page.click("text=Select Load Combinations")
        await page.check("input[value='1.2D + 1.6L']")
        await page.check("input[value='1.2D + 1.0W']")
        await page.click("text=Confirm")
        
        await page.click("text=Create Analysis")
        await page.wait_for_selector("text=Analysis created successfully")
        
        # Run the analysis
        await page.click("text=Run Analysis")
        await page.wait_for_selector("text=Analysis completed successfully", timeout=30000)
        
        # Create P-Delta analysis
        await page.click("text=New Analysis")
        await page.fill("input[placeholder='Analysis Name']", "P-Delta Analysis")
        await page.select_option("select[name='analysis_type']", "p_delta")
        await page.check("input[name='include_p_delta']")
        
        # Select load combinations
        await page.click("text=Select Load Combinations")
        await page.check("input[value='1.2D + 1.6L']")
        await page.check("input[value='1.2D + 1.0W']")
        await page.click("text=Confirm")
        
        await page.click("text=Create Analysis")
        await page.wait_for_selector("text=Analysis created successfully")
        
        # Run the analysis
        await page.click("text=Run Analysis")
        await page.wait_for_selector("text=Analysis completed successfully", timeout=30000)
        
        # Create modal analysis
        await page.click("text=New Analysis")
        await page.fill("input[placeholder='Analysis Name']", "Modal Analysis")
        await page.select_option("select[name='analysis_type']", "modal")
        await page.fill("input[name='num_modes']", "10")
        
        await page.click("text=Create Analysis")
        await page.wait_for_selector("text=Analysis created successfully")
        
        # Run the analysis
        await page.click("text=Run Analysis")
        await page.wait_for_selector("text=Analysis completed successfully", timeout=30000)
        
        # Step 8: View analysis results
        print("Viewing analysis results...")
        await page.click("text=Results")
        
        # Select the P-Delta analysis
        await page.select_option("select[name='analysis_id']", "P-Delta Analysis")
        await page.select_option("select[name='load_combination_id']", "1.2D + 1.0W")
        
        # View deformed shape
        await page.click("text=Deformed Shape")
        await page.wait_for_selector("canvas")
        await asyncio.sleep(3)  # Wait to see the visualization
        
        # View element forces
        await page.click("text=Element Forces")
        await page.wait_for_selector("canvas")
        await asyncio.sleep(3)
        
        # View modal results
        await page.select_option("select[name='analysis_id']", "Modal Analysis")
        await page.click("text=Modal Results")
        await page.wait_for_selector("text=Mode 1")
        await asyncio.sleep(3)
        
        # Step 9: Run design checks
        print("Running design checks...")
        await page.click("text=Design")
        
        # Create new design
        await page.click("text=New Design")
        await page.fill("input[placeholder='Design Name']", "AISC 360-16 Design")
        await page.select_option("select[name='design_code']", "aisc_360_16")
        await page.select_option("select[name='design_method']", "lrfd")
        
        # Select analysis to use
        await page.select_option("select[name='analysis_id']", "P-Delta Analysis")
        
        # Select load combinations
        await page.click("text=Select Load Combinations")
        await page.check("input[value='1.2D + 1.6L']")
        await page.check("input[value='1.2D + 1.0W']")
        await page.click("text=Confirm")
        
        await page.click("text=Create Design")
        await page.wait_for_selector("text=Design created successfully")
        
        # Run the design
        await page.click("text=Run Design")
        await page.wait_for_selector("text=Design completed successfully", timeout=30000)
        
        # View design results
        await page.click("text=Design Results")
        await page.wait_for_selector("text=Unity Ratio")
        await asyncio.sleep(3)
        
        # Step 10: Generate detailing
        print("Generating detailing...")
        await page.click("text=Detailing")
        
        # Create new detailing
        await page.click("text=New Detailing")
        await page.fill("input[placeholder='Detailing Name']", "Steel Connections")
        await page.select_option("select[name='design_id']", "AISC 360-16 Design")
        
        await page.click("text=Create Detailing")
        await page.wait_for_selector("text=Detailing created successfully")
        
        # Run the detailing
        await page.click("text=Generate Details")
        await page.wait_for_selector("text=Detailing completed successfully", timeout=30000)
        
        # View connection details
        await page.click("text=Connection Details")
        await page.wait_for_selector("text=Beam-to-Column Connections")
        await asyncio.sleep(3)
        
        # Step 11: View BIM model
        print("Viewing BIM model...")
        await page.click("text=BIM")
        
        # Create BIM model
        await page.click("text=New BIM Model")
        await page.fill("input[placeholder='Model Name']", "10-Story Building Model")
        await page.click("text=Create Model")
        await page.wait_for_selector("text=BIM Model created successfully")
        
        # Generate geometry
        await page.click("text=Generate Geometry")
        await page.wait_for_selector("text=Geometry generated successfully", timeout=30000)
        
        # View 3D model
        await page.click("text=View 3D Model")
        await page.wait_for_selector("canvas")
        
        # Interact with the 3D model
        await page.mouse.move(960, 540)  # Center of the screen
        await page.mouse.down()
        await page.mouse.move(1060, 540, steps=10)  # Rotate
        await page.mouse.up()
        await asyncio.sleep(2)
        
        await page.mouse.wheel(0, -200)  # Zoom in
        await asyncio.sleep(2)
        
        await page.mouse.wheel(0, 400)  # Zoom out
        await asyncio.sleep(2)
        
        # Take a screenshot
        screenshot_path = os.path.join(RECORDING_PATH, "bim_model.png")
        await page.screenshot(path=screenshot_path)
        
        # Close browser
        await context.close()
        await browser.close()
        
        print("Test completed successfully!")


if __name__ == "__main__":
    asyncio.run(test_10_story_building())