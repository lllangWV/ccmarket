# AGENTS.md Anti-Patterns

Common mistakes when writing AGENTS.md and why they fail.

## Instruction Stuffing

**Bad:**
```markdown
## Code Style
- Use camelCase for functions
- Use PascalCase for types
- Always add JSDoc comments
- Use async/await not promises
- Prefer const over let
- Use destructuring when possible
- Always handle errors with try/catch
- Use early returns
- Keep functions under 20 lines
[... 50 more rules ...]
```

**Why it fails:**
- Bloats instruction count toward the ~150 limit
- Degrades instruction-following uniformly across ALL instructions
- Most rules only apply to specific tasks
- LLMs learn style from the codebase anyway

**Fix:** Use linters. Remove style guidelines entirely.

## Embedded Code Snippets

**Bad:**
```markdown
## Patterns

Always structure components like this:
```tsx
export const Button: React.FC<ButtonProps> = ({ label, onClick }) => {
  const [isHovered, setIsHovered] = useState(false);

  const handleClick = useCallback(() => {
    if (onClick) {
      onClick();
    }
  }, [onClick]);

  return (
    <button
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      onClick={handleClick}
      className={cn(styles.button, isHovered && styles.hovered)}
    >
      {label}
    </button>
  );
};
```
```

**Why it fails:**
- Becomes stale as codebase evolves
- Bloats context window
- Takes up instruction budget
- Real codebase is the authoritative source

**Fix:** Use `file:line` pointers: "See `src/components/Button.tsx:15` for component pattern"

## Task-Specific Instructions

**Bad:**
```markdown
## Database

When creating new tables:
1. Add migration in migrations/
2. Update schema in prisma/schema.prisma
3. Run prisma generate
4. Update the seed file
5. Add types to src/types/database.ts

When querying:
1. Use the repository pattern
2. Always use transactions for writes
3. Index foreign keys
[... more database instructions ...]
```

**Why it fails:**
- Only relevant when doing database work
- Goes into EVERY conversation, even unrelated ones
- Wastes context and instruction budget on frontend tasks

**Fix:** Put in `specs/database.md`. Add pointer in AGENTS.md:
```markdown
| Database | `specs/database.md` |
```

## Everything in One File

**Bad:**
```markdown
# Project

[500 lines covering everything: architecture, APIs, database,
deployment, testing, code style, git workflow, troubleshooting...]
```

**Why it fails:**
- Exceeds instruction-following capacity
- Most content irrelevant to any single task
- Claude ignores content it deems irrelevant
- Irrelevant content causes ignoring of relevant content too

**Fix:** Progressive disclosure structure:
```
AGENTS.md           # <100 lines, universal only
specs/README.md     # Index of all specs
specs/*.md          # Detailed per-domain specs
docs/*.md           # Operational guides
```

## Vague Instructions

**Bad:**
```markdown
## Guidelines

- Follow best practices
- Write clean code
- Be consistent
- Use appropriate patterns
```

**Why it fails:**
- Zero actionable information
- Wastes instruction slots
- "Best practices" means nothing without context

**Fix:** Either be specific or omit entirely. LLMs already try to write good code.

## Duplicating Linter Rules

**Bad:**
```markdown
## Formatting

- Use 2-space indentation
- Max line length 80 characters
- Use single quotes for strings
- Add trailing commas
- No semicolons
```

**Why it fails:**
- Linters do this deterministically
- LLMs are slow and expensive for formatting
- These rules already exist in config files

**Fix:** Configure linter. Add pre-commit hook. Remove from AGENTS.md entirely.

## Auto-Generated Content

**Bad:**
Using `/init` or similar to auto-generate AGENTS.md.

**Why it fails:**
- AGENTS.md is highest leverage point
- Auto-generation creates bloated, generic content
- Generic content gets ignored
- Every bad line affects every task

**Fix:** Manually craft every line. Treat it like the most important code in your repo.

## Conditional Instructions

**Bad:**
```markdown
## API Development

If building a REST endpoint:
- Use Express router
- Add validation middleware
- Follow REST conventions

If building a GraphQL resolver:
- Use type-graphql decorators
- Add input validation
- Follow cursor-based pagination

If building a WebSocket handler:
- Use socket.io rooms
- Implement heartbeat
- Handle reconnection
```

**Why it fails:**
- Only one branch applies per task
- All branches consume instruction budget
- Conditional logic wastes context

**Fix:** Put each in separate spec files. Let agent read relevant one when needed.

## Missing Pointers

**Bad:**
```markdown
# Project

## Commands
[commands]

## Structure
[structure]

[No mention of specs/ or docs/]
```

**Why it fails:**
- Agent doesn't know detailed docs exist
- Can't use progressive disclosure if unaware of resources
- Reinvents context that's already documented

**Fix:** Always include Documentation section pointing to specs/ and docs/.
