---
title: Prototype Demo
description: Testing Astro + shadcn/ui integration with sample content
---

import DocumentationCard from '../../components/DocumentationCard.astro'

# DeepResearchAgent Documentation Prototype

This page demonstrates the Astro + Starlight + shadcn/ui integration for the documentation prototype.

## Component Integration Test

<DocumentationCard
  title="TUI Implementation"
  status="in-progress"
  description="Terminal User Interface development using Textual framework - Phase 1 priority"
>

The TUI development is currently in progress using the Textual framework. This represents the **primary development priority** and must be completed before advancing the documentation prototype.

Key components include:
- Interactive task input system
- Real-time progress monitoring
- Professional terminal interface
- Integration with existing DeepResearchAgent core

</DocumentationCard>

<DocumentationCard
  title="Astro Documentation Foundation"
  status="completed"
  description="Modern documentation system with Astro + Starlight + Tailwind + shadcn/ui"
>

The foundation for the new documentation system has been successfully implemented:

- ✅ Astro 5.x with Starlight theme
- ✅ Tailwind CSS 4.x integration
- ✅ React support for shadcn/ui components
- ✅ TypeScript configuration with import aliases
- ✅ Essential UI components (Button, Card, Badge)

</DocumentationCard>

<DocumentationCard
  title="Content Migration"
  status="pending"
  description="Migration of existing documentation to new Astro system"
>

Content migration is planned for after TUI completion:

1. **Phase 1**: TUI planning documents (test content)
2. **Phase 2**: Core documentation (AGENTS.md, README.md)
3. **Phase 3**: Session reports and detailed specifications
4. **Phase 4**: Complete migration and system cutover

</DocumentationCard>

## Technology Stack

The prototype leverages modern web technologies while maintaining performance:

### Core Framework
- **Astro 5.6.1** - Islands Architecture for optimal performance
- **Starlight** - Professional documentation theme
- **TypeScript** - Type safety and better developer experience

### Styling & Components
- **Tailwind CSS 4.x** - Utility-first CSS framework
- **shadcn/ui** - High-quality React components
- **Radix UI** - Accessible component primitives

### Performance Benefits
- **Zero JavaScript by default** - Static HTML generation
- **Selective hydration** - Interactive components only when needed
- **Modern CSS** - CSS variables for efficient theming

## Build Pipeline

The new system integrates with the existing cost-optimized approach:

```bash
# Development
npm run dev      # Local development server

# Production
npm run build    # Generate static files
npm run preview  # Preview production build
```

## Future Capabilities

This foundation enables advanced features for future development:

- **Interactive data visualizations** (D3.js integration ready)
- **Client-side data processing** (DuckDB-Wasm integration points)
- **Progressive enhancement** patterns
- **Mobile-responsive** documentation experience

---

**Status**: Foundation complete, awaiting TUI completion for next phase development.