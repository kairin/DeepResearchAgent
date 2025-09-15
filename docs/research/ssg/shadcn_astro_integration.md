# shadcn/ui + Astro Integration Research

> **Research Date**: September 16, 2025
> **Purpose**: Document integration patterns for shadcn/ui components with Astro framework
> **Priority**: Foundation research for documentation prototype

## 🎯 Integration Challenge Analysis

### **Core Challenge**
shadcn/ui is designed primarily for React-based projects, while Astro is framework-agnostic. The challenge is integrating React-based shadcn/ui components into Astro's Islands Architecture without losing performance benefits.

### **Astro's React Integration Model**
Astro supports React through its integration system:
- Components are **static by default** (no JavaScript shipped)
- JavaScript only loads when `client:*` directives are used
- Supports selective hydration (Islands Architecture)

## 🔧 Integration Strategies

### **Strategy 1: Direct React Integration (Recommended)**

**Setup Process:**
1. ✅ Install Astro React integration: `npx astro add react`
2. ✅ Install Tailwind CSS: `npx astro add tailwind`
3. Install shadcn/ui: `npx shadcn@latest init`
4. Configure components for Astro environment

**Component Usage Pattern:**
```astro
---
// src/components/ui/Button.astro
import { Button } from '@/components/ui/button'
---

<!-- Static by default -->
<Button>Static Button</Button>

<!-- Interactive when needed -->
<Button client:load>Interactive Button</Button>
```

### **Strategy 2: Astro Component Wrappers**

Create Astro wrapper components for common shadcn/ui patterns:
```astro
---
// src/components/DocumentationCard.astro
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

interface Props {
  title: string;
  content: string;
  interactive?: boolean;
}

const { title, content, interactive = false } = Astro.props;
---

<Card class="documentation-card" client:load={interactive}>
  <CardHeader>
    <CardTitle>{title}</CardTitle>
  </CardHeader>
  <CardContent>
    <p>{content}</p>
  </CardContent>
</Card>
```

### **Strategy 3: Selective Hydration for Interactive Elements**

Use client directives strategically:
- `client:load` - Hydrate immediately
- `client:idle` - Hydrate when browser idle
- `client:visible` - Hydrate when visible
- `client:media` - Hydrate based on media query

```astro
<!-- Static documentation layout -->
<Layout>
  <!-- Interactive search component -->
  <SearchDialog client:idle />

  <!-- Static content -->
  <DocumentationContent />

  <!-- Interactive data visualization -->
  <DataChart client:visible />
</Layout>
```

## 📋 Technical Implementation Plan

### **Phase 1: Basic shadcn/ui Setup**

#### **Step 1: Initialize shadcn/ui**
```bash
cd astro-docs
npx shadcn@latest init
```

**Configuration Options:**
- TypeScript: Yes (already configured)
- Style: Default
- Base color: Slate
- CSS variables: Yes

#### **Step 2: Install Core Components**
```bash
# Essential components for documentation
npx shadcn@latest add button card input label
npx shadcn@latest add navigation-menu sheet sidebar
npx shadcn@latest add dialog dropdown-menu command
```

#### **Step 3: Configure Tailwind for Starlight Integration**
Create custom CSS overrides for Starlight + shadcn/ui compatibility:

```css
/* src/styles/shadcn-starlight.css */
@import '@tailwindcss/base';
@import '@tailwindcss/components';
@import '@tailwindcss/utilities';

/* Override Starlight styles where needed */
.sl-container {
  @apply max-w-none;
}

/* shadcn/ui component overrides for documentation theme */
.documentation-card {
  @apply border-border bg-card text-card-foreground;
}
```

### **Phase 2: Component Architecture**

#### **Component Organization**
```
src/
├── components/
│   ├── ui/                 # shadcn/ui components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   └── ...
│   ├── astro/              # Astro wrapper components
│   │   ├── DocumentationCard.astro
│   │   ├── InteractiveSearch.astro
│   │   └── NavigationMenu.astro
│   └── islands/            # Interactive islands
│       ├── SearchDialog.tsx
│       └── ThemeToggle.tsx
```

#### **Wrapper Component Pattern**
```astro
---
// src/components/astro/DocumentationSection.astro
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'

interface Props {
  title: string;
  status: 'planning' | 'in-progress' | 'completed';
  children: any;
}

const { title, status } = Astro.props;
---

<Card class="mb-6">
  <CardHeader>
    <div class="flex items-center justify-between">
      <CardTitle>{title}</CardTitle>
      <Badge variant={status === 'completed' ? 'default' : status === 'in-progress' ? 'secondary' : 'outline'}>
        {status}
      </Badge>
    </div>
  </CardHeader>
  <CardContent>
    <slot />
  </CardContent>
</Card>
```

### **Phase 3: Performance Optimization**

#### **Bundle Optimization**
- Use `client:idle` for non-critical interactive components
- Minimize hydrated components on initial page load
- Implement code splitting for large interactive features

#### **Build Configuration**
```javascript
// astro.config.mjs
export default defineConfig({
  integrations: [
    starlight({
      // Starlight config
    }),
    react()
  ],
  vite: {
    plugins: [tailwindcss()],
    build: {
      rollupOptions: {
        output: {
          manualChunks: {
            'shadcn-ui': ['@/components/ui'],
            'react-islands': ['@/components/islands']
          }
        }
      }
    }
  }
});
```

## 🚨 Known Issues & Solutions

### **Issue 1: CSS Conflicts with Starlight**
**Problem**: Starlight has its own styling system that may conflict with Tailwind/shadcn
**Solution**:
- Use CSS specificity to override Starlight styles
- Create custom CSS layer for shadcn components
- Test component rendering in Starlight context

### **Issue 2: SSR Hydration Mismatches**
**Problem**: React components may have hydration issues in Astro
**Solution**:
- Use `client:only` for components with browser-specific logic
- Ensure component props are serializable
- Avoid browser APIs in component initial render

### **Issue 3: Build Time Performance**
**Problem**: Adding React + shadcn/ui may slow builds (addressing Astro weakness)
**Solution**:
- Monitor build times with content volume
- Use Astro's selective hydration to minimize JavaScript
- Implement build caching strategies

## 🎯 Documentation Use Cases

### **Primary Components for Documentation**
1. **Navigation**: Sidebar, navigation menu, breadcrumbs
2. **Content**: Cards, badges, alerts, tabs
3. **Search**: Command palette, search dialog
4. **Interactive**: Theme toggle, copy-to-clipboard buttons
5. **Layout**: Grid, containers, separators

### **Example: Documentation Card Component**
```astro
---
// Usage in documentation pages
import DocumentationCard from '@/components/astro/DocumentationCard.astro'
---

<DocumentationCard
  title="TUI Implementation"
  status="in-progress"
>
  <p>Terminal User Interface development using Textual framework...</p>

  <!-- Interactive element only when needed -->
  <ProgressTracker client:visible />
</DocumentationCard>
```

## 📊 Performance Expectations

### **Bundle Size Impact**
- **Baseline Astro + Starlight**: ~50KB JavaScript
- **With React + shadcn/ui**: ~150KB JavaScript (selective hydration)
- **Mitigation**: Use Islands Architecture to minimize hydrated components

### **Build Time Impact**
- **Expected increase**: 20-30% longer builds with React integration
- **Mitigation**:
  - Monitor build times as content scales
  - Implement incremental builds
  - Use build caching

## ✅ Next Steps

1. **Initialize shadcn/ui** in Astro project
2. **Create wrapper components** for common documentation patterns
3. **Test integration** with existing Starlight theme
4. **Benchmark performance** against current documentation system
5. **Document migration patterns** for existing content

---

**Research Status**: Foundation complete - ready for implementation testing
**Risk Assessment**: Medium complexity, well-documented integration patterns exist
**Recommendation**: Proceed with cautious implementation, monitoring build performance