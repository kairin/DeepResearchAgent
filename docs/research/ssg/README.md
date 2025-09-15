# Static Site Generator Research & Implementation

> **Status**: Research Phase - Foundation for Astro-based documentation prototype
> **Priority**: TUI implementation takes precedence - this runs in parallel
> **Target**: Documentation-focused prototype with future interactive capabilities

## 📋 Research Documentation Index

### **Comparative Analysis**
- [`astro_comparative_analysis.md`](./astro_comparative_analysis.md) - Comprehensive analysis of Astro's strengths and weaknesses compared to other SSGs
- [`interactive_data_sites_analysis.md`](./interactive_data_sites_analysis.md) - Technical analysis for client-side data applications with DuckDB-Wasm and D3.js

### **Key Research Findings**

#### **Astro Strengths (for our use case):**
- ✅ Islands Architecture - minimal JS by default
- ✅ Framework agnostic - can integrate React for shadcn/ui
- ✅ Excellent performance for content-driven sites
- ✅ Zero JavaScript shipping unless explicitly needed
- ✅ Strong markdown and content collection support

#### **Astro Weaknesses (to mitigate):**
- ⚠️ Build time scalability (22.90s for 4000 files vs Hugo's 0.68s)
- ⚠️ Learning curve for non-JS developers
- ⚠️ Complex abstractions can obscure granular control

#### **Strategic Mitigation Approaches:**
1. **Start small** - Prototype with existing content volume (~30 files)
2. **Monitor build times** - Implement optimization from day one
3. **Gradual complexity** - Begin with static docs, add interactivity later
4. **Local CI/CD** - Maintain cost control with existing approach

## 🎯 Implementation Strategy

### **Technology Stack Decision**
Based on research and requirements:

```
Framework: Astro 4.x + Starlight (official docs template)
Styling: Tailwind CSS (integrated with Starlight)
Components: shadcn/ui (React integration for interactive elements)
Language: TypeScript (better DX, future maintenance)
Content: Existing markdown structure (migrated gradually)
Build: Local CI/CD pipeline (cost-optimized)
Deploy: GitHub Pages (parallel to existing system)
```

### **Parallel Development Approach**
```
Current System (Active):
└── docs/ + scripts/build_docs.sh + GitHub Pages

Astro Prototype (Development):
└── astro-docs/ + scripts/build_astro.sh + Separate GitHub Pages branch
```

### **Content Migration Strategy**
1. **Phase 1**: TUI planning documents (rich content for testing)
2. **Phase 2**: Core documentation (AGENTS.md, README.md, etc.)
3. **Phase 3**: Session reports and detailed specs
4. **Phase 4**: Complete migration and cutover

## 🔧 Technical Implementation Plan

### **Foundation Setup (Current Phase)**
- [x] Research document organization
- [ ] Astro + Starlight prototype creation
- [ ] Tailwind CSS integration research
- [ ] shadcn/ui + Astro compatibility analysis
- [ ] Local build pipeline design

### **Prototype Development (After TUI Phase 1)**
- [ ] Basic Astro setup with existing content subset
- [ ] shadcn/ui component integration
- [ ] Tailwind styling system
- [ ] Content collection structure
- [ ] Build time optimization

### **Integration & Deployment (After TUI Completion)**
- [ ] GitHub Pages integration
- [ ] Local CI/CD pipeline
- [ ] Performance benchmarking
- [ ] Content migration automation
- [ ] System cutover planning

## 🚧 Current Blockers & Dependencies

### **Immediate Dependencies:**
- **TUI Phase 1 completion** - Primary project priority
- **Node.js ecosystem setup** - Required for Astro development
- **shadcn/ui + Astro integration research** - Technical feasibility confirmation

### **Future Dependencies:**
- **Content migration tooling** - Automated migration scripts
- **Build optimization** - Performance monitoring and tuning
- **Interactive feature requirements** - DuckDB-Wasm + D3.js integration specs

## 📊 Success Criteria

### **Foundation Phase (Current):**
- ✅ Research documents organized and accessible
- ✅ Implementation strategy documented
- ✅ Technical stack validated
- [ ] Prototype structure created
- [ ] Build pipeline designed

### **Prototype Phase:**
- [ ] Astro + Starlight + Tailwind + shadcn/ui integration working
- [ ] Existing content renders correctly
- [ ] Build times acceptable (< 30 seconds for current content)
- [ ] Local CI/CD pipeline functional
- [ ] GitHub Pages deployment successful

### **Production Phase:**
- [ ] Feature parity with current documentation system
- [ ] Performance improvements over current system
- [ ] Foundation ready for interactive feature additions
- [ ] Zero disruption to current workflow during transition

## 🔗 Related Documentation

- [TUI Planning Documentation](../../planning/tui/) - Primary development focus
- [Current Build System](../../../scripts/) - Existing local CI/CD approach
- [Documentation Standards](../../standards/) - Content organization guidelines

## 🌐 Project Websites

- **Fork Documentation**: [https://kairin.github.io/DeepResearchAgent/](https://kairin.github.io/DeepResearchAgent/) - Enhanced documentation with TUI development, migration guides, and implementation planning
- **Original Research**: [https://skyworkai.github.io/DeepResearchAgent/](https://skyworkai.github.io/DeepResearchAgent/) - Foundational architecture, experiments, and academic research

---

**Note**: This research and planning work proceeds in parallel with TUI development but does not take priority. All foundation work is preparatory for post-TUI implementation.