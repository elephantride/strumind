import { pgTable, text, serial, integer, boolean, real, timestamp } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

export const users = pgTable("users", {
  id: serial("id").primaryKey(),
  username: text("username").notNull().unique(),
  password: text("password").notNull(),
});

export const projects = pgTable("projects", {
  id: serial("id").primaryKey(),
  name: text("name").notNull(),
  description: text("description"),
  userId: integer("user_id").notNull(),
  createdAt: timestamp("created_at").defaultNow(),
  updatedAt: timestamp("updated_at").defaultNow(),
});

export const nodes = pgTable("nodes", {
  id: serial("id").primaryKey(),
  projectId: integer("project_id").notNull(),
  nodeId: text("node_id").notNull(),
  x: real("x").notNull(),
  y: real("y").notNull(),
  z: real("z").notNull(),
});

export const elements = pgTable("elements", {
  id: serial("id").primaryKey(),
  projectId: integer("project_id").notNull(),
  elementId: text("element_id").notNull(),
  elementType: text("element_type").notNull(),
  startNodeId: text("start_node_id").notNull(),
  endNodeId: text("end_node_id").notNull(),
  sectionType: text("section_type").notNull(),
  materialType: text("material_type").notNull(),
  length: real("length"),
});

export const loadCases = pgTable("load_cases", {
  id: serial("id").primaryKey(),
  projectId: integer("project_id").notNull(),
  name: text("name").notNull(),
  description: text("description"),
  loadType: text("load_type").notNull(),
  isActive: boolean("is_active").default(true),
});

export const analysisResults = pgTable("analysis_results", {
  id: serial("id").primaryKey(),
  projectId: integer("project_id").notNull(),
  elementId: text("element_id").notNull(),
  loadCaseId: integer("load_case_id").notNull(),
  axialForce: real("axial_force"),
  shearY: real("shear_y"),
  shearZ: real("shear_z"),
  momentY: real("moment_y"),
  momentZ: real("moment_z"),
  maxDisplacement: real("max_displacement"),
  maxStress: real("max_stress"),
});

export const designResults = pgTable("design_results", {
  id: serial("id").primaryKey(),
  projectId: integer("project_id").notNull(),
  elementId: text("element_id").notNull(),
  sectionType: text("section_type").notNull(),
  designCode: text("design_code").notNull(),
  axialCheck: real("axial_check"),
  momentCheck: real("moment_check"),
  unityCheck: real("unity_check"),
  status: text("status").notNull(),
  governingCheck: text("governing_check"),
});

export const insertUserSchema = createInsertSchema(users).pick({
  username: true,
  password: true,
});

export const insertProjectSchema = createInsertSchema(projects).pick({
  name: true,
  description: true,
  userId: true,
});

export const insertNodeSchema = createInsertSchema(nodes).pick({
  projectId: true,
  nodeId: true,
  x: true,
  y: true,
  z: true,
});

export const insertElementSchema = createInsertSchema(elements).pick({
  projectId: true,
  elementId: true,
  elementType: true,
  startNodeId: true,
  endNodeId: true,
  sectionType: true,
  materialType: true,
  length: true,
});

export const insertLoadCaseSchema = createInsertSchema(loadCases).pick({
  projectId: true,
  name: true,
  description: true,
  loadType: true,
  isActive: true,
});

export type InsertUser = z.infer<typeof insertUserSchema>;
export type User = typeof users.$inferSelect;
export type InsertProject = z.infer<typeof insertProjectSchema>;
export type Project = typeof projects.$inferSelect;
export type InsertNode = z.infer<typeof insertNodeSchema>;
export type Node = typeof nodes.$inferSelect;
export type InsertElement = z.infer<typeof insertElementSchema>;
export type Element = typeof elements.$inferSelect;
export type InsertLoadCase = z.infer<typeof insertLoadCaseSchema>;
export type LoadCase = typeof loadCases.$inferSelect;
export type AnalysisResult = typeof analysisResults.$inferSelect;
export type DesignResult = typeof designResults.$inferSelect;
