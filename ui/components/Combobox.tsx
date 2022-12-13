/*
  This example requires some changes to your config:
  
  ```
  // tailwind.config.js
  module.exports = {
    // ...
    plugins: [
      // ...
      require('@tailwindcss/forms'),
    ],
  }
  ```
*/
import { Combobox } from '@headlessui/react';
import { CheckIcon, ChevronUpDownIcon } from '@heroicons/react/20/solid';
import { useState } from 'react';

function classNames(...classes: any[]) {
  return classes.filter(Boolean).join(' ');
}

// https://tailwindui.com/components/application-ui/forms/comboboxes
// https://headlessui.com/react/combobox
export default function TailwindCombobox<T>({
  selectedDatabase,
  handleSelectionChange,
  databases,
  render,
}: {
  selectedDatabase: T | undefined;
  handleSelectionChange: (arg0: T) => void;
  databases: T[];
  render: (arg0: T) => string;
}) {
  const [query, setQuery] = useState('');
  const isDisabled = databases.length === 0;

  const filteredDatabases: T[] =
    query === ''
      ? databases
      : databases.filter(person => {
          return render(person).toLowerCase().includes(query.toLowerCase());
        });

  return (
    <Combobox
      as="div"
      value={selectedDatabase}
      onChange={handleSelectionChange}
      className="w-full sm: w-1/4"
      disabled={isDisabled}>
      <Combobox.Label className="block text-sm font-medium text-gray-700">
        <h2 className="text-sm text-gray-400 my-1 mx-4">Select workflow:</h2>
      </Combobox.Label>
      <div className="relative mt-1">
        <Combobox.Input
          className="w-full rounded-md border border-gray-300 bg-white py-2 pl-3 pr-10 shadow-sm focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 sm:text-sm"
          onChange={event => setQuery(event.target.value)}
          displayValue={(person: T) => render(person)}
          // defaultValue
          // placeholder={'Waiting for you to select...'}
        />
        <Combobox.Button className="absolute inset-y-0 right-0 flex items-center rounded-r-md px-2 focus:outline-none">
          <ChevronUpDownIcon className="h-5 w-5 text-gray-400" aria-hidden="true" />
        </Combobox.Button>

        {filteredDatabases.length > 0 && (
          <Combobox.Options className="absolute z-10 mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm">
            {filteredDatabases.map(person => (
              <Combobox.Option
                key={render(person)}
                value={person}
                className={({ active }) =>
                  classNames(
                    'relative cursor-default select-none py-2 pl-3 pr-9',
                    active ? 'bg-indigo-600 text-white' : 'text-gray-900'
                  )
                }>
                {({ active, selected }) => (
                  <>
                    <span className={classNames('block truncate', selected && 'font-semibold')}>
                      {render(person)}
                    </span>

                    {selected && (
                      <span
                        className={classNames(
                          'absolute inset-y-0 right-0 flex items-center pr-4',
                          active ? 'text-white' : 'text-indigo-600'
                        )}>
                        <CheckIcon className="h-5 w-5" aria-hidden="true" />
                      </span>
                    )}
                  </>
                )}
              </Combobox.Option>
            ))}
          </Combobox.Options>
        )}
      </div>
    </Combobox>
  );
}
