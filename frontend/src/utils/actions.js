export const scrollToTop = (id) => {
    const elem =  document.getElementById(id)
    if (elem) {
        elem.scrollIntoView()
    }
}