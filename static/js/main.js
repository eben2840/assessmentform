const button = document.querySelector('button')
const heading = document.querySelector('h1')


const isDark = document.documentElement.dataset.theme === 'dark' || matchMedia('(prefers-color-scheme: dark)').matches
heading.innerText = `Now with ${isDark ? 'Light' : 'Dark'} Mode.`
button.setAttribute('aria-pressed', isDark ? false : true)
document.documentElement.dataset.theme = isDark ? 'dark' : 'light'

const sync = () => {
  const darkNow = button.matches('[aria-pressed=false]')
  document.documentElement.dataset.theme = darkNow ? 'light' : 'dark'
  heading.innerText = `Now with ${darkNow ? 'Dark' : 'Light'} Mode.`
  button.setAttribute('aria-pressed', darkNow ? true : false)
}

const handleSync = () => {
  if (!document.startViewTransition) return sync()
  document.startViewTransition(sync)
}

button.addEventListener('click', handleSync)
