export const POST_LISTING_FORM_FIELDS = [
    {
        name: 'title',
        type: "text",
        placeholder: 'List title',
        label: 'Title',
        required: true,
        initialValue: ''
    },
    {
        name: 'description',
        type: "textarea",
        placeholder: 'List description',
        label: 'Description',
        initialValue: ''
    },
    {
        name: 'price',
        type: "price",
        label: 'Price',
        defaultValue: 0,
        required: true,
        initialValue: 0,
    },
    {
        name: 'is_price_negotiable',
        type: "checkbox",
        label: 'Negotiable',
        initialValue: false,
    },
    {
        name: 'files',
        type: 'files',
        label: 'Upload Files',
        initialValue: [],
        required: true, 
    }
]